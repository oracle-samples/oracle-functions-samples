#
# oci-objectstorage-copy-objects-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#
import io
import json
import logging

import oci.object_storage
from fdk import response

def copy_object(signer, namespace, src_bucket, dst_bucket, object_name):
    try:
        objstore = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
        objstore_composite_ops = oci.object_storage.ObjectStorageClientCompositeOperations(objstore)
        resp = objstore_composite_ops.copy_object_and_wait_for_state(
            namespace, 
            src_bucket, 
            oci.object_storage.models.CopyObjectDetails(
                destination_bucket=dst_bucket, 
                destination_namespace=namespace,
                destination_object_name=object_name,
                destination_region=signer.region,
                source_object_name=object_name
            )
        )
    except (Exception, ValueError) as ex:
        logging.getLogger().error(str(ex))
        return {"response": str(ex)}

    return {"response": str(response)}


def handler(ctx, data: io.BytesIO=None):
    signer = oci.auth.signers.get_resource_principals_signer()
    resp   = ""
    try:
        body        = json.loads(data.getvalue())
        #logging.getLogger().info(json.dumps(body))
        namespace   = body["data"]["additionalDetails"]["namespace"]
        src_bucket  = body["data"]["additionalDetails"]["bucketName"]
        object_name = body["data"]["resourceName"]
        dst_bucket  = body["data"]["additionalDetails"]["bucketName"]+"_IMMUTABLE"

        logging.getLogger().info(f'Copying {object_name} from {src_bucket} to {dst_bucket}')

        resp = copy_object(signer, namespace, src_bucket, dst_bucket, object_name)
    except (Exception, ValueError) as ex:
        logging.getLogger().error(str(ex))
 
    return response.Response(
        ctx, 
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
