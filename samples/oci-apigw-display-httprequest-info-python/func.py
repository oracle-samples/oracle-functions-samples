#
# oci-apigw-display-httprequest-info-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import oci
import logging
from urllib.parse import urlparse, parse_qs

from fdk import response


def handler(ctx, data: io.BytesIO=None):
    logging.getLogger().info("function handler start")
    
    resp = {}

    # retrieving the request headers
    headers = ctx.Headers()
    logging.getLogger().info("Headers: " + json.dumps(headers))
    resp["Headers"] = headers

    # retrieving the function configuration
    resp["Configuration"] = dict(ctx.Config())
    logging.getLogger().info("Configuration: " + json.dumps(resp["Configuration"]))

    # retrieving the request body, e.g. {"key1":"value"}
    #requestbody_bytes = data.getvalue()
    #if requestbody_bytes==b'':
    #    logging.getLogger().info("No request body")
    #    requestbody = {}
    #else:
    #    requestbody = json.loads(requestbody_bytes)
    #    logging.getLogger().info()
    try:
        requestbody_str = data.getvalue().decode('UTF-8')
        if requestbody_str:
            resp["Request body"] = json.loads(requestbody_str)
        else:
            resp["Request body"] = {}
    except Exception as ex:
        print('ERROR: The request body is not JSON', ex, flush=True)
        raise

    # retrieving the request URL, e.g. "/v1/display-uri-info"
    requesturl = ctx.RequestURL()
    logging.getLogger().info("Request URL: " + json.dumps(requesturl))
    resp["Request URL"] = requesturl
    
    # retrieving query string from the request URL, e.g. {"param1":["value"]}
    parsed_url = urlparse(requesturl)
    resp["Query String"] = parse_qs(parsed_url.query)
    logging.getLogger().info("Query string: " + json.dumps(resp["Query String"]))

    # retrieving the request method, e.g. "POST", "GET"...
    method = ctx.Method()
    if method:
        logging.getLogger().info("Request Method: " + method)
        resp["Request Method"] = method
    else:
        logging.getLogger().info("No Request Method")
        resp["Request Method"] = None

    # retrieving the Application ID, e.g. "ocid1.fnapp.oc1.phx.aaaaxxxx"
    appid = ctx.AppID()
    logging.getLogger().info("AppID: " + appid)
    resp["AppID"] = appid

    # retrieving the Function ID, e.g. "ocid1.fnfunc.oc1.phx.aaaaxxxxx"
    fnid = ctx.FnID()
    logging.getLogger().info("FnID: " + fnid)
    resp["FnID"] = fnid

    # retrieving the Function call ID, e.g. "01E9FE6JBW1BT0C68ZJ003KR1Q"
    callid = ctx.CallID()
    logging.getLogger().info("CallID: " + callid)
    resp["CallID"] = callid

    # retrieving the Function format, e.g. "http-stream"
    fnformat = ctx.Format()
    logging.getLogger().info("Format: " + fnformat)
    resp["Format"] = fnformat

    # retrieving the Function deadline, e.g. "2020-05-29T05:24:46Z"
    deadline = ctx.Deadline()
    logging.getLogger().info("Deadline: " + deadline)
    resp["Deadline"] = deadline

    logging.getLogger().info("function handler end")
    return response.Response(
        ctx, 
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
