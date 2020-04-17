#
# imagedims-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import tempfile

from fdk import response
from wand.image import Image

def handler(ctx, data: io.BytesIO=None):
    resp = {}
    with tempfile.TemporaryFile() as tempf:
        tempf.write(data.getbuffer())
        tempf.seek(0)
        with Image(file = tempf) as img:
            resp["width"] = img.width
            resp["height"] = img.height

    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
