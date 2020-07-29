#
# oci-event-display-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json

from fdk import response

def handler(ctx, data: io.BytesIO=None):
    try:
        body = json.loads(data.getvalue())
        print("event type: " + body["eventType"])
        print("compartment name: " + body["data"]["compartmentName"])
        print("Full Cloud event json data:")
        print(json.dumps(body, indent=4), flush=True)
    except (Exception) as ex:
        print('ERROR: Missing key in payload', ex, flush=True)
        raise

    return response.Response(
        ctx,
        response_data=json.dumps(body),
        headers={"Content-Type": "application/json"}
    )