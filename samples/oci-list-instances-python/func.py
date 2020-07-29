#
# oci-list-instances-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
from fdk import response

import oci

def handler(ctx, data: io.BytesIO=None):
    signer = oci.auth.signers.get_resource_principals_signer()
    resp = list_instances(signer)
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

# List instances ---------------------------------------------------------------
def list_instances(signer):
    client = oci.core.ComputeClient(config={}, signer=signer)
    # OCI API to manage Compute resources such as compute instances, block storage volumes, etc.
    try:
        # Returns a list of all instances in the current compartment
        inst = client.list_instances(signer.compartment_id)
        # Create a list that holds a list of the instances id and name next to each other
        inst = [[i.id, i.display_name] for i in inst.data]
    except Exception as ex:
        print("ERROR: accessing Compute instances failed", ex, flush=True)
        raise
    resp = { "instances": inst }
    return resp
