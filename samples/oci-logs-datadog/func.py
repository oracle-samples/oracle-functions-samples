#
# oci-logs-datadog version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import oci
import os
import json
import requests
import logging
from fdk import response


"""
This Function receives the logging json and invokes the Datadog endpoint for ingesting logs.
Logging Format Overview https://docs.cloud.oracle.com/en-us/iaas/Content/Logging/Reference/top_level_logging_format.htm#top_level_logging_format
If this Function is invoked with more than one log the function go over each log and invokes the Datadog endpoint for ingesting one by one.
"""
def handler(ctx, data: io.BytesIO=None):
    try:
        logs = json.loads(data.getvalue())

#       go over each log and invokes the Datadog endpoint for ingesting one by one.
        for item in logs: 
       
#           Datadog endpoint URL and token to call the REST interface. These values are defined in func.yaml
            datadoghost = os.environ['DATADOG_HOST']
            datadogtoken = os.environ['DATADOG_TOKEN']

#           Call the Datadog with the payload.
            headers = {'Content-type': 'application/json', 'DD-API-KEY': datadogtoken}
            x = requests.post(datadoghost, data = json.dumps(item), headers=headers)
            logging.getLogger().info(x.text)
       
    except (Exception, ValueError) as ex:
        logging.getLogger().info(str(ex))
        return
