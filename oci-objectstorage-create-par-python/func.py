#
# oci-objectstorage-create-par-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
from fdk import response
import oci.object_storage
from datetime import datetime, timedelta

def create_PAR(signer, bucket_name, PAR_name, lifetime):
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = client.get_namespace().data
    par_expiration = datetime.utcnow() + timedelta(minutes=lifetime)
    object_storage_endpoint = "https://objectstorage." + signer.region + ".oraclecloud.com"
    par_details = oci.object_storage.models.CreatePreauthenticatedRequestDetails(name=PAR_name, access_type='AnyObjectWrite', time_expires=par_expiration)
    par = client.create_preauthenticated_request(namespace_name=namespace, bucket_name=bucket_name, create_preauthenticated_request_details=par_details)
    par_url = object_storage_endpoint + par.data.access_uri
    return par_url

def handler(ctx, data: io.BytesIO=None):
    signer = oci.auth.signers.get_resource_principals_signer()
    bucket_name = PAR_name = ""
    lifetime = 0
    try:
        cfg = ctx.Config()
        bucket_name = cfg["bucket-name"]
        lifetime = int(cfg["lifetime"])
    except Exception as e:
        print('Missing function parameters: bucket-name and lifetime (in minutes)', flush=True)
        raise
    try:
        body = json.loads(data.getvalue())
        PAR_name = body["PAR name"]
    except Exception as e:
        print('Input a JSON object with the format: \'{"PAR name": "<PAR name>"}\' ', flush=True)
        raise
    par_url = create_PAR(signer, bucket_name, PAR_name, lifetime)
    return response.Response(
        ctx,
        response_data=json.dumps({"PAR URL": par_url}),
        headers={"Content-Type": "application/json"}
    )
