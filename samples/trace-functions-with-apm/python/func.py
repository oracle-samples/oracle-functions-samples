#
# trace-functions-with-apm-python version 1.0.
#
# Copyright (c) 2021 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl
#

import io
import json
import logging
from fdk import response
import requests

#
# The following imports are required. Includ py_zipkin and requests in the requirements.txt file.
#
from py_zipkin import Encoding
from py_zipkin.zipkin import zipkin_span

# this method is used by the zipkin library to emit spans to the apm endpoint, data key is included in this url.
def apm_transport_handler(encoded_span):
    logging.getLogger().info("Inside app: " + app_name + " | function: " + func_name + " | method: apm_transport_handler")
    return requests.post(
        apm_domain_url,
        data=encoded_span,
        headers={'Content-Type': 'application/json'},
    )


# this is the entry point of the function
def handler(ctx, data: io.BytesIO = None):
    global app_name, func_name, apm_domain_url, apm_service_name, apm_binary_annotations
    app_name = ctx.AppName()
    func_name = ctx.FnName()
    logging.getLogger().info("Inside app: " + app_name + " | function: " + func_name + " | method: handler")
    tracing_context = ctx.TracingContext()
    apm_domain_url = tracing_context.trace_collector_url()
    apm_service_name = tracing_context.service_name()
    logging.getLogger().info("Inside app: " + app_name + " | function: " + func_name + " | method: handler | apm_service_name: " + apm_service_name)
    apm_binary_annotations = tracing_context.annotations()

    with zipkin_span(
        service_name = apm_service_name,
        span_name = "handler method (custom child span)",
        transport_handler = apm_transport_handler,
        zipkin_attrs = tracing_context.zipkin_attrs(),
        encoding = Encoding.V2_JSON,
        binary_annotations = apm_binary_annotations
    ):
        # this is the actual unit of work performed by the function
        message = say_hello(data)
        logging.getLogger().info("Inside app: " + app_name + " | function: " + func_name + " | method: handler | returned message: " + message)
        return response.Response(
            ctx, response_data=json.dumps(
                {"message": message}),
            headers={"Content-Type": "application/json"}
        )

# Here's an example of showing an error in a child span.
# In this example, if we do not receive a name in the input message body,
# we will show an error in the span, and return a hello greeting using 
# a default name instead.
def say_hello(data: io.BytesIO = None):
    logging.getLogger().info("Inside app: " + app_name + " | function: " + func_name + " | method: say_hello")
    with zipkin_span(
        service_name = apm_service_name,
        span_name = "say_hello method (custom child span)",
        binary_annotations = apm_binary_annotations
    ) as span_context:
        name = "OCI Functions-APM integration!"
        try:
            body = json.loads(data.getvalue())
            name = body.get("name")
        except (Exception, ValueError) as ex:
            logging.getLogger().info("Inside app: " + app_name + " | function: " + func_name + " | method: say_hello | error parsing json payload: " + str(ex))
            errors = {
                "Error": True,
                "ErrorMessage": str(ex)
                }
            span_context.update_binary_annotations(errors)

        message = "Hello {0}".format(name)
        logging.getLogger().info("message: " + message)
        return message
