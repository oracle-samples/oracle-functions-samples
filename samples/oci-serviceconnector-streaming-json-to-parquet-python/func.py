#
# oci-serviceconnector-streaming-json-to-parquet-python version 1.0.
#
# Copyright (c) 2021 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import os
import oci
import json
import requests
import logging
import base64
import gzip
import time
import pandas as pd
from fdk import response


"""
This Function converts JSON to Parquet format and uploads the file to Object storage
"""
def handler(ctx, data: io.BytesIO=None):
    logger = logging.getLogger()

    namespace = os.environ['NAME_SPACE']
    bucket_name = os.environ['BUCKET_NAME']
    file_name = os.environ['FILE_NAME'] + time.strftime("%Y%m%d%H%M%S") + '.gz'

    try:
        logs = json.loads(data.getvalue())
        logger.info('Received {} entries.'.format(len(logs)))

        for item in logs:
            if 'value' in item:
                item['value'] = base64_decode(item['value'])

            if 'key' in item:
                item['key'] = base64_decode(item['key'])

        df = pd.json_normalize(logs)
        parquet_result = df.to_parquet(index=False)
        file_compress = gzip.compress(parquet_result)
        upload_file(namespace, bucket_name, file_name, file_compress)
 
        return

    except (Exception, ValueError) as e:
        logger.error(str(e))
        raise


def base64_decode(encoded):
    if encoded != '' and encoded is not None:
        base64_bytes = encoded.encode('utf-8')
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('utf-8')


def upload_file(namespace, bucket_name, file_name, f):
    assert bucket_name and file_name
    signer = oci.auth.signers.get_resource_principals_signer()
    object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    object_storage.put_object(namespace, bucket_name, file_name, f)
    return 
