#
# oci-logs-splunk-hec version 0.1.
#
# Copyright (c) 2024 Splunk, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import os
import json
import requests
import logging
from fdk import response


"""
This Function receives the logging json and forwards to the Splunk HTTP Event
Connector (HEC) for ingesting logs. Logging Format Overview
https://docs.cloud.oracle.com/en-us/iaas/Content/Logging/Reference/top_level_logging_format.htm#top_level_logging_format
If this Function is invoked with more than one log the function go over each log and invokes the HEC endpoint for ingesting one by one.
"""

def handler(ctx, data: io.BytesIO=None):
    try:
        logs = json.loads(data.getvalue())

        # no need to have verbose logs from log forwarder
        urllib3_logger = logging.getLogger('urllib3')
        urllib3_logger.setLevel(logging.CRITICAL)

        # Splunk HEC endpoint URL and token to call the REST interface. These values are defined in func.yaml
        hec_endpoint = os.environ['SPLUNK_HEC_ENDPOINT']
        hec_token = os.environ['SPLUNK_HEC_TOKEN']
        headers = {'Content-type': 'application/json', 'Authorization': str("Splunk " + str(hec_token))}

        # loop over each log and reformat for HEC.
        concat_body = ""
        for item in logs:
            event = item['oracle']
            event.update(item['data'])
            body = {}
            body['event'] = event
            body['source'] = 'oci:' + item['source']
            body['sourcetype'] = '_json'
            concat_body = concat_body + str(json.dumps(body))

        # Post the message to HEC payload.
        if len(concat_body) > 0:
            x = requests.post(hec_endpoint, data = concat_body, headers=headers)
            if x.status_code != 200:
                logging.getLogger().info(x.text)

    except (Exception, ValueError) as ex:
        logging.getLogger().info(str(ex))
    return
