#
# oci-notification-syniverse version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import os
import oci
import json
import requests
import logging
import datetime
import base64
from fdk import response


"""
This Function receives the logging json and invokes the Syniverse endpoint for send a SMS.
Logging Format Overview https://docs.cloud.oracle.com/en-us/iaas/Content/Logging/Reference/top_level_logging_format.htm#top_level_logging_format
If this Function is invoked with more than one log the function go over each log and invokes the Syniverse endpoint for send one by one.
"""
def handler(ctx, data: io.BytesIO=None):
    try:
        namespace = os.environ['SYNIVERSE_NAMESPACE']
        bucket_name = os.environ['SYNIVERSE_BUCKET_NAME']
        object_name = os.environ['SYNIVERSE_OBJECT_NAME']
        phones = request_one_object(namespace, bucket_name, object_name)

        signer = oci.auth.signers.get_resource_principals_signer()
        secret_client = oci.secrets.SecretsClient(config={}, signer=signer)

        secret_token = os.environ['SYNIVERSE_TOKEN']
        response_token = read_secret_value(secret_client, secret_token)
        response_host = os.environ['SYNIVERSE_HOST']
        response_channel = os.environ['SYNIVERSE_CHANNEL']

#       Syniverse endpoint URL and token to call the REST interface. This values are defined in functionalists.yaml
        syniversehost = response_host
        syniversetoken = "Bearer " + response_token
        syniversechannel = "channel:" + response_channel

        logs = json.loads(data.getvalue())
        for item in logs:
            body = "OCI SCH Notification: "
#           get json type and time information
            if "source" in item:
                body = body + item.get("source")
            else:
                body = body + " - "

            if "id" in item:
                body = body + "Id: " + item.get("id")

            if "oracle.tenantid" in item:
                body = body + "\nTenancy: " + item.get("oracle.tenantid")

            if "time" in item:
                body = body + "\nTime: " + item.get("time")

            payload = {}
            payload.update({"from":syniversechannel})
            payload.update({"to":phones.split(',')})
            payload.update({"body":body})

#           Call the Syniverse with the payload.
            headers = {'Content-type': 'application/json', 'authorization': syniversetoken}
            requests.post(syniversehost, data = json.dumps(payload), headers=headers, timeout=2)

    except (Exception, ValueError) as e:
        logging.error(e)
        return


"""
Retrieve values from Oracle vault
This Function reads the Syniverse API token that is secrete storege in Oracle Vault.
The oracle vault toke used to retriave the value is defined on func.yaml file
"""
def read_secret_value(secret_client, secret_id):
    response = secret_client.get_secret_bundle(secret_id)
    base64_Secret_content = response.data.secret_bundle_content.content
    base64_secret_bytes = base64_Secret_content.encode('ascii')
    base64_message_bytes = base64.b64decode(base64_secret_bytes)
    secret_content = base64_message_bytes.decode('ascii')
    return secret_content


"""
Read file from Object Store.
This Function reads the file with target phones to send the SMS. 
The path and the file name is defined on func.yaml file
"""
def request_one_object(namespace, bucket_name, object_name):
    assert bucket_name and object_name
    signer = oci.auth.signers.get_resource_principals_signer()
    object_storage_client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    get_obj = object_storage_client.get_object(namespace, bucket_name, object_name)
    file_content = ''
    for chunk in get_obj.data.raw.stream(1024 * 1024, decode_content=True):
        file_content = file_content + str(chunk, 'utf-8')
    return file_content.strip()