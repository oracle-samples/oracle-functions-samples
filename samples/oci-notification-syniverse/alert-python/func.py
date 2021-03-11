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
This Function receives the Oracle Notification json and invokes the Syniverse endpoint for send a SMS.
"""
def handler(ctx, data: io.BytesIO=None):
    try:
        # read the target phones file
        namespace = os.environ['SYNIVERSE_NAMESPACE']
        bucket_name = os.environ['SYNIVERSE_BUCKET_NAME']
        object_name = os.environ['SYNIVERSE_OBJECT_NAME']
        phones = request_one_object(namespace, bucket_name, object_name)
        log = json.loads(data.getvalue()) 

#       get and parse the json body
        if "body" in log:
            body = log.get("body")
        else:
            body = ""

        if "title" in log:
            body = body + ": " + log.get("title")

        if "type" in log:
            body = body + " has entered " + log.get("type") + " state."

        if "severity" in log:
            body = body + "\nSeverity: " + log.get("severity")
        
        if "timestampEpochMillis" in log:
            time_in_millis = log.get("timestampEpochMillis") / 1000.0
            dt = datetime.datetime.fromtimestamp(time_in_millis).strftime('%Y-%m-%d %H:%M')
            body = body + "\nTime: " + dt

        signer = oci.auth.signers.get_resource_principals_signer()
        secret_client = oci.secrets.SecretsClient(config={}, signer=signer)

        secret_token = os.environ['SYNIVERSE_TOKEN']
        response_token = read_secret_value(secret_client, secret_token)
        response_host = os.environ['SYNIVERSE_HOST']
        response_channel = os.environ['SYNIVERSE_CHANNEL']

#       Syniverse endpoint URL and token to call the REST interface. This values are defined in func.yaml
        syniversehost = response_host
        syniversetoken = "Bearer " + response_token
        syniversechannel = "channel:" + response_channel

        payload = {}
        payload.update({"from":syniversechannel})
        payload.update({"to":phones.split(',')})
        payload.update({"body":body})

#       Call the Syniverse with the payload. adjust the timeout value for your case
        headers = {'Content-type': 'application/json', 'authorization': syniversetoken}
        requests.post(syniversehost, data = json.dumps(payload), headers=headers, timeout=2)

       
    except (Exception, ValueError) as e:
        # add your error handler here
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