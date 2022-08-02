#
# oci-monitoring-metrics-to-datadog version 1.0.
#
# Copyright (c) 2022, Oracle and/or its affiliates. All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.

import io
import json
import logging
import os
import re
import requests
from fdk import response
from datetime import datetime

"""
This sample OCI Function maps OCI Monitoring Service Metrics to the DataDog 
REST API 'submit-metrics' contract found here:

https://docs.datadoghq.com/api/latest/metrics/#submit-metrics

"""

# Use OCI Application or Function configurations to override these environment variable defaults.

api_endpoint = os.getenv('DATADOG_METRICS_API_ENDPOINT', 'not-configured')
api_key = os.getenv('DATADOG_API_KEY', 'not-configured')
is_forwarding = eval(os.getenv('FORWARD_TO_DATADOG', "True"))
metric_tag_keys = os.getenv('METRICS_TAG_KEYS', 'name, namespace, displayName, resourceDisplayName, unit')
metric_tag_set = set()

# Set all registered loggers to the configured log_level

logging_level = os.getenv('LOGGING_LEVEL', 'INFO')
loggers = [logging.getLogger()] + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
[logger.setLevel(logging.getLevelName(logging_level)) for logger in loggers]

# Exception stack trace logging

is_tracing = eval(os.getenv('ENABLE_TRACING', "False"))

# Constants

TEN_MINUTES_SEC = 10 * 60
ONE_HOUR_SEC = 60 * 60

# Functions

def handler(ctx, data: io.BytesIO = None):
    """
    OCI Function Entry Point
    :param ctx: InvokeContext
    :param data: data payload
    :return: plain text response indicating success or error
    """

    preamble = " {} / event count = {} / logging level = {} / forwarding to DataDog = {}"

    try:
        metrics_list = json.loads(data.getvalue())
        logging.getLogger().info(preamble.format(ctx.FnName(), len(metrics_list), logging_level, is_forwarding))
        logging.getLogger().debug(metrics_list)
        converted_event_list = handle_metric_events(event_list=metrics_list)
        send_to_datadog(event_list=converted_event_list)

    except (Exception, ValueError) as ex:
        logging.getLogger().error('error handling logging payload: {}'.format(str(ex)))
        if is_tracing:
            logging.getLogger().error(ex)


def handle_metric_events(event_list):
    """
    :param event_list: the list of metric formatted log records.
    :return: the list of DataDog formatted log records
    """

    result_list = []
    for event in event_list:
        single_result = transform_metric_to_datadog_format(log_record=event)
        result_list.append(single_result)
        logging.getLogger().debug(single_result)

    return result_list


def transform_metric_to_datadog_format(log_record: dict):
    """
    Transform metrics to DataDog format.
    See: https://github.com/metrics/spec/blob/v1.0/json-format.md
    :param log_record: metric log record
    :return: DataDog formatted log record
    """

    series = [{
        'metric': get_metric_name(log_record),
        'type' : get_metric_type(log_record),
        'points' : get_metric_points(log_record),
        'tags' : get_metric_tags(log_record),
    }]

    result = {
        'series' : series
    }
    return result


def get_metric_name(log_record: dict):
    """
    Assembles a metric name that appears to follow DataDog conventions.
    :param log_record:
    :return:
    """

    elements = get_dictionary_value(log_record, 'namespace').split('_')
    elements += camel_case_split(get_dictionary_value(log_record, 'name'))
    elements = [element.lower() for element in elements]
    return '.'.join(elements)


def camel_case_split(str):
    """
    :param str:
    :return: Splits camel case string to individual strings
    """

    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)


def get_metric_type(log_record: dict):
    """
    :param log_record:
    :return: The type of metric. The available types are 0 (unspecified), 1 (count), 2 (rate), and 3 (gauge).
    Allowed enum values: 0,1,2,3
    """

    return 0


def get_now_timestamp():
    return datetime.now().timestamp()


def adjust_metric_timestamp(timestamp_ms):
    """
    DataDog Timestamps should be in POSIX time in seconds, and cannot be more than ten
    minutes in the future or more than one hour in the past.  OCI Timestamps are POSIX
    in milliseconds, therefore a conversion is required.

    See https://docs.datadoghq.com/api/latest/metrics/#submit-metrics
    :param oci_timestamp:
    :return:
    """

    # positive skew is expected
    timestamp_sec = int(timestamp_ms / 1000)
    delta_sec = get_now_timestamp() - timestamp_sec

    if (delta_sec > 0 and delta_sec > ONE_HOUR_SEC):
        logging.getLogger().warning('timestamp {} too far in the past per DataDog'.format(timestamp_ms))

    if (delta_sec < 0 and abs(delta_sec) > TEN_MINUTES_SEC):
        logging.getLogger().warning('timestamp {} too far in the future per DataDog'.format(timestamp_ms))

    return timestamp_sec


def get_metric_points(log_record: dict):
    """
    :param log_record:
    :return: an array of arrays where each array is a datapoint scalar pair
    """

    result = []

    datapoints = get_dictionary_value(dictionary=log_record, target_key='datapoints')
    for point in datapoints:
        dd_point = {'timestamp': adjust_metric_timestamp(point.get('timestamp')),
                    'value': point.get('value')}

        result.append(dd_point)

    return result


def get_metric_tags(log_record: dict):
    """
    Assembles tags from selected metric attributes.
    See https://docs.datadoghq.com/getting_started/tagging/
    :param log_record: the log record to scan
    :return: string of comma-separated, key:value pairs matching DataDog tag format
    """

    result = []

    for tag in get_metric_tag_set():
        value = get_dictionary_value(dictionary=log_record, target_key=tag)
        if value is None:
            continue

        if isinstance(value, str) and ':' in value:
            logging.getLogger().warning('tag contains a \':\' / ignoring {} ({})'.format(key, value))
            continue

        tag = '{}:{}'.format(tag, value)
        result.append(tag)

    return result


def get_metric_tag_set():
    """
    :return: the set metric payload keys that we would like to have converted to tags.
    """

    global metric_tag_set

    if len(metric_tag_set) == 0 and metric_tag_keys:
        split_and_stripped_tags = [x.strip() for x in metric_tag_keys.split(',')]
        metric_tag_set.update(split_and_stripped_tags)
        logging.getLogger().debug("tag key set / {} ".format (metric_tag_set))

    return metric_tag_set


def send_to_datadog (event_list):
    """
    Sends each transformed event to DataDog Endpoint.
    :param event_list: list of events in DataDog format
    :return: None
    """

    if is_forwarding is False:
        logging.getLogger().debug("DataDog forwarding is disabled - nothing sent")
        return

    if 'v2' not in api_endpoint:
        raise RuntimeError('Requires API endpoint version "v2": "{}"'.format(api_endpoint))

    # creating a session and adapter to avoid recreating
    # a new connection pool between each POST call

    try:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10)
        session.mount('https://', adapter)

        for event in event_list:
            api_headers = {'Content-type': 'application/json', 'DD-API-KEY': api_key}
            logging.getLogger().debug("json to datadog: {}".format (json.dumps(event)))
            response = session.post(api_endpoint, data=json.dumps(event), headers=api_headers)

            if response.status_code != 202:
                raise Exception ('error {} sending to DataDog: {}'.format(response.status_code, response.reason))

    finally:
        session.close()


def get_dictionary_value(dictionary: dict, target_key: str):
    """
    Recursive method to find value within a dictionary which may also have nested lists / dictionaries.
    :param dictionary: the dictionary to scan
    :param target_key: the key we are looking for
    :return: If a target_key exists multiple times in the dictionary, the first one found will be returned.
    """

    if dictionary is None:
        raise Exception('dictionary None for key'.format(target_key))

    target_value = dictionary.get(target_key)
    if target_value:
        return target_value

    for key, value in dictionary.items():
        if isinstance(value, dict):
            target_value = get_dictionary_value(dictionary=value, target_key=target_key)
            if target_value:
                return target_value

        elif isinstance(value, list):
            for entry in value:
                if isinstance(entry, dict):
                    target_value = get_dictionary_value(dictionary=entry, target_key=target_key)
                    if target_value:
                        return target_value


def local_test_mode(filename):
    """
    This routine reads a local json metrics file, converting the contents to DataDog format.
    :param filename: cloud events json file exported from OCI Logging UI or CLI.
    :return: None
    """

    logging.getLogger().info("local testing started")

    with open(filename, 'r') as f:
        transformed_results = list()

        for line in f:
            event = json.loads(line)
            logging.getLogger().debug(json.dumps(event, indent=4))
            transformed_result = transform_metric_to_datadog_format(event)
            transformed_results.append(transformed_result)

        logging.getLogger().debug(json.dumps(transformed_results, indent=4))
        send_to_datadog(event_list=transformed_results)

    logging.getLogger().info("local testing completed")


"""
Local Debugging 
"""

if __name__ == "__main__":
    local_test_mode('oci-metrics-test-file.json')

