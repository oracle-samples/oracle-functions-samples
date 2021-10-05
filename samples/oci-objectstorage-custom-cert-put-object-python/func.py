#
# oci-objectstorage-onsr-put-object-python version 1.0.
#
# Copyright (c) 2021 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import os
import json
import sys
from fdk import response

import oci.object_storage

# Certs location
cert_file_path = "/etc/oci-pki/customer/customer-cert.pem"
# file to upload
file_to_upload = "cert_test"
file_to_upload_content = {"content":"This is test file"}

def handler(ctx, data: io.BytesIO=None):
    try:
        body = json.loads(data.getvalue())
        bucketName = body["bucketName"]
    except Exception:
        error = """
                Input a JSON object in the format: '{"bucketName": "<bucket name>",
                "content": "<content>", "objectName": "<object name>"}'
                """
        raise Exception(error)
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    if os.path.exists(cert_file_path):
        client.base_client.session.verify = cert_file_path

    resp = put_object(client, bucketName, file_to_upload, file_to_upload_content)
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

def put_object(client, bucketName, objectName, content):
    namespace = client.get_namespace().data
    output=""
    try:
        object = client.put_object(namespace, bucketName, objectName, json.dumps(content))
        output = "Success: Put object '" + objectName + "' in bucket '" + bucketName + "'"
    except Exception as e:
        output = "Failed: " + str(e.message)
    return { "state": output }
