#
# oci-monitoring-metrics-to-splunk-observability version 0.1.
#
# Copyright (c) 2024, Splunk, Inc. All rights reserved.
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
This sample OCI Function maps OCI Monitoring Service Metrics to the Splunk
Observability REST API '/datapoint' contract found here:

https://dev.splunk.com/observability/reference/api/ingest_data/latest#endpoint-send-metrics

"""

# Use OCI Application or Function configurations to override these environment variable defaults.

api_token = os.getenv('SPLUNK_O11Y_TOKEN', 'not-configured')
api_realm = os.getenv('SPLUNK_O11Y_REALM', 'us0')
is_forwarding = eval(os.getenv('FORWARD_TO_SPLUNK_O11Y', "True"))

# Set all registered loggers to the configured log_level

logging_level = os.getenv('LOGGING_LEVEL', 'INFO')
loggers = [logging.getLogger()] + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
[logger.setLevel(logging.getLevelName(logging_level)) for logger in loggers]

# Exception stack trace logging

is_tracing = eval(os.getenv('ENABLE_TRACING', "False"))

# Constants

TEN_MINUTES_MSEC = 10 * 60 * 1000
ONE_HOUR_MSEC = 60 * 60 * 1000

# Functions

def handler(ctx, data: io.BytesIO = None):
    """
    OCI Function Entry Point
    :param ctx: InvokeContext
    :param data: data payload
    :return: plain text response indicating success or error
    """

    preamble = " {} / event count = {} / logging level = {} / forwarding to Splunk = {}"

    try:
        metrics_list = json.loads(data.getvalue())
        logging.getLogger().info(preamble.format(ctx.FnName(), len(metrics_list), logging_level, is_forwarding))
        logging.getLogger().debug(metrics_list)
        converted_events = handle_metric_events(event_list=metrics_list)
        send_to_splunk_o11y(events=converted_events)

    except (Exception, ValueError) as ex:
        logging.getLogger().error('error handling logging payload: {}'.format(str(ex)))
        if is_tracing:
            logging.getLogger().error(ex)


def handle_metric_events(event_list):
    """
    :param event_list: the list of metric formatted log records.
    :return: the list of Splunk Observability formatted log records
    """

    result_list = []
    for event in event_list:
        list_result = transform_metric_to_splunk_o11y_format_list(log_record=event)
        result_list.extend(list_result)
        logging.getLogger().debug(list_result)

    return result_list


def transform_metric_to_splunk_o11y_format_list(log_record: dict):
    """
    Transform metrics to Splunk Observability format. OCI does not define metric
    types, so all OCI metrics are presented as gauge type.
    See: https://dev.splunk.com/observability/reference/api/ingest_data/latest#endpoint-send-metrics
    :param log_record: metric log record
    :return: Splunk Observability json datapoint record
    """

    o11y_dps = []
    datapoints = get_dictionary_value(dictionary=log_record, target_key='datapoints')
    metric_name = get_dictionary_value(log_record, 'name')
    metric_dims = get_metric_dimensions(log_record)
    for point in datapoints:
        o11y_dp = {
            'metric': metric_name,
            'value' : point.get('value'),
            'dimensions' : metric_dims,
            'timestamp' : point.get('timestamp')
        }
        o11y_dps.append(o11y_dp)

    ordered_dps = sorted(o11y_dps, key=lambda dp: dp['timestamp'])
    return ordered_dps


def get_metric_dimensions(log_record: dict):
    """
    Assembles dimensions from selected metric attributes.
    :param log_record: the log record to scan
    :return: dictionary of dimensions meeting Splunk Observability semantics
    """

    result = {}

    # context dimensions

    result['oci_namespace'] = get_dictionary_value(dictionary=log_record, target_key="namespace")
    result['oci_compartment_id'] = get_dictionary_value(dictionary=log_record, target_key="compartmentId")
    unit = get_dictionary_value(dictionary=log_record, target_key="unit")
    if unit is not None:
        result['oci_unit'] = unit
    rg = get_dictionary_value(dictionary=log_record, target_key="resourceGroup")
    if rg is not None:
        result['oci_namespace'] = rg

    dim_dict = get_dictionary_value(dictionary=log_record, target_key="dimensions")
    for dim in dim_dict.items():
        if fix_dimension_value(dim[1]) is not None:
            result[ fix_dimension_name('oci_dim_' + str(dim[0])) ] = fix_dimension_value( dim[1] )

    return result


def fix_dimension_name (name):
    nowhitespace = ((str(name).strip()).replace(' ',''))
    noleadunderscores = nowhitespace.lstrip('_')
    noquotes = (noleadunderscores.replace('\"', '_')).replace('\'','_')
    nottoolong = noquotes[:128]
    return nottoolong


def fix_dimension_value (value):
    nowhitespace = (str(value)).strip()
    noquotes = (nowhitespace.replace('\"', '_')).replace('\'','_')
    nottoolong = noquotes[:256]
    return nottoolong


def send_to_splunk_o11y (events):
    """
    Sends each transformed event to Splunk Observability Endpoint.
    :param events: list of events in Splunk Observability format
    :return: None
    """

    if is_forwarding is False:
        logging.getLogger().debug("Splunk Observability forwarding is disabled - nothing sent")
        return

    # creating a session and adapter to avoid recreating
    # a new connection pool between each POST call

    try:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10)
        session.mount('https://', adapter)

        api_headers = {'Content-Type': 'application/json', 'X-SF-Token': api_token}
        sorted_events = sorted(events, key=lambda dp: dp['timestamp'])
        message_body = {'gauge' : sorted_events}
        logging.getLogger().debug("json to splunk observability: {}".format (json.dumps(message_body)))
        logging.getLogger().debug("headers to splunk observability: {}".format (json.dumps(api_headers)))
        post_url = 'https://ingest.%s.signalfx.com/v2/datapoint' % (api_realm)
        logging.getLogger().debug("post to splunk observability: {}".format (post_url))
        response = session.post(post_url, data=json.dumps(message_body), headers=api_headers)

        if response.status_code != 200:
            raise Exception ('error {} sending to Splunk Observability: {}'.format(response.status_code, response.reason))

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

    for _, value in dictionary.items():
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
    This routine reads a local json metrics file, converting the contents to Splunk Observability format.
    :param filename: cloud events json file exported from OCI Logging UI or CLI.
    :return: None
    """

    logging.getLogger().info("local testing started")

    with open(filename, 'r') as f:
        transformed_results = list()

        for line in f:
            event = json.loads(line)
            logging.getLogger().debug(json.dumps(event, indent=4))
            transformed_result = transform_metric_to_splunk_o11y_format_list(event)
            transformed_results.append(transformed_result)

        logging.getLogger().debug(json.dumps(transformed_results, indent=4))
        send_to_splunk_o11y(events=transformed_results)

    logging.getLogger().info("local testing completed")


"""
Local Debugging
"""

if __name__ == "__main__":
    local_test_mode('oci-metrics-test-file.json')
