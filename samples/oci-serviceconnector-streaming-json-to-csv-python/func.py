#
# oci-serviceconnector-streaming-json-to-csv-python version 1.0.
#
# Copyright (c) 2021 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import oci
import json
import requests
import logging
import base64
import pandas as pd
from fdk import response


"""
This Function converts JSON to CSV format
"""
def handler(ctx, data: io.BytesIO=None):
    logger = logging.getLogger()

    try:
        logs = json.loads(data.getvalue())
        logger.info('Received {} entries.'.format(len(logs)))

        for item in logs:
            if 'value' in item:
                item['value'] = base64_decode(item['value'])

            if 'key' in item:
                item['key'] = base64_decode(item['key'])

        df = pd.json_normalize(logs)
        csv_result = df.to_csv(index=False)
        return response.Response(ctx, status_code=200, response_data=csv_result, headers={"Content-Type": "text/csv"})
    
    except (Exception, ValueError) as e:
        logger.error(str(e))
        raise


def base64_decode(encoded):
    print(type(encoded))
    base64_bytes = encoded.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')