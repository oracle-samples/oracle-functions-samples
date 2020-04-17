#
# oci-invoke-function version 1.0.
#
# Copyright (c) 2019 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import oci
from fdk import response

def handler(ctx, data: io.BytesIO=None):
    try:
        body = json.loads(data.getvalue())
        function_endpoint = body.get("function_endpoint")
        function_ocid = body.get("function_ocid")
        function_body = body.get("function_body")
    except (Exception) as ex:
        print('ERROR: Missing key in payload', ex, flush=True)
        raise
    
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.functions.FunctionsInvokeClient(config={}, signer=signer, service_endpoint=function_endpoint)
    resp = client.invoke_function(function_id=function_ocid, invoke_function_body=function_body)
    print(resp.data.text, flush=True)

    return response.Response(
        ctx, 
        response_data=resp.data.text,
        headers={"Content-Type": "application/json"}
    )