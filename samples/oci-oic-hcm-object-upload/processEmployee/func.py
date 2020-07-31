#
# oci-oic-hsm-object-upload version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

from fdk import response
import os
import io
import json
import sys
import oci.object_storage


def handler(ctx, data: io.BytesIO = None):

    signer = oci.auth.signers.get_resource_principals_signer()

    try:
        cfg = ctx.Config()
        cfg_namespace = cfg["OCI_NAMESPACE"]
        cfg_bucketname = cfg["OCI_BUCKETNAME"]
    except Exception as ex:
        print("Error: Configuration key has not been set.", ex, flush=True)
        raise

    try:
        info = json.load(data)
        firstname = info.get("firstname")
        lastname = info.get("lastname")
        workemail = info.get("workemail")
        hiredate = info.get("hiredate")
        effectivestartdate = info.get("effectivestartdate")
        personid = info.get("personid")

    except (Exception, ValueError) as ex:
        return str(ex)

    filename = personid + "_data.csv"
    personinfo = personid + ", " + firstname + ", " + lastname + ", " + workemail + ", " + hiredate + ", " + effectivestartdate

    return_output = put_object(signer, cfg_bucketname, filename, personinfo, cfg_namespace=cfg_namespace)
    return response.Response(
        ctx,
        response_data=json.dumps(return_output),
        headers={"Content-Type": "application/json"}
    )


def put_object(signer, bucketname, objectname, content, cfg_namespace):
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    try:
        client.put_object(cfg_namespace, bucketname, objectname, content)
        output = "Success State"
    except Exception as e:
        output = "Failed State"
    response = {"state": output}
    return response

