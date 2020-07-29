#
# oci-ons-compute-shape-increase-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import oci

from fdk import response

def increase_compute_shape(instance_id, alarm_msg_shape):
    signer = oci.auth.signers.get_resource_principals_signer()
    compute_client = oci.core.ComputeClient(config={}, signer=signer)
    current_shape = compute_client.get_instance(instance_id).data.shape
    print("INFO: current shape for Instance {0}: {1}".format(instance_id,current_shape), flush=True)
    if current_shape != alarm_msg_shape:
        return "The shape of Instance {} differs from the Alarm message".format(instance_id)
    # improve the logic below to handle more scenarios, make sure the shapes you select are available in the region and AD
    if  current_shape == "VM.Standard1.1":
        new_shape = "VM.Standard2.1"
    elif current_shape == "VM.Standard2.1":
        new_shape = "VM.Standard2.2"
    else:
        return "Instance {0} cannot get a bigger shape than its current shape {1}".format(instance_id,current_shape)
    print("INFO: new shape for Instance {0}: {1}".format(instance_id,new_shape), flush=True)
    try:
        update_instance_details = oci.core.models.UpdateInstanceDetails(shape=new_shape)
        resp = compute_client.update_instance(instance_id=instance_id, update_instance_details=update_instance_details)
        print(resp, flush=True)
    except Exception as ex:
        print('ERROR: cannot update instance {}'.format(instance_id), flush=True)
        raise
    return "The shape of Instance {} is updated, the instance is rebooting...".format(instance_id)

def handler(ctx, data: io.BytesIO=None):
    alarm_msg = {}
    message_id = func_response = ""
    try:
        headers = ctx.Headers()
        message_id = headers["x-oci-ns-messageid"]
    except Exception as ex:
        print('ERROR: Missing Message ID in the header', ex, flush=True)
        raise
    print("INFO: Message ID = ", message_id, flush=True)
    # the Message Id can be stored in a database and be used to check for duplicate messages
    try:
        alarm_msg = json.loads(data.getvalue())
        print("INFO: Alarm message: ")
        print(alarm_msg, flush=True)
    except (Exception, ValueError) as ex:
        print(str(ex), flush=True)

    if alarm_msg["type"] == "OK_TO_FIRING":
        if alarm_msg["alarmMetaData"][0]["dimensions"]:
            alarm_metric_dimension = alarm_msg["alarmMetaData"][0]["dimensions"][0]   #assuming the first dimension matches the instance to resize
            print("INFO: Instance to resize: ", alarm_metric_dimension["resourceId"], flush=True)
            func_response = increase_compute_shape(alarm_metric_dimension["resourceId"], alarm_metric_dimension["shape"])
            print("INFO: ", func_response, flush=True)
        else:
            print('ERROR: There is no metric dimension in this alarm message', flush=True)
            func_response = "There is no metric dimension in this alarm message"
    else:
        print('INFO: Nothing to do, alarm is not FIRING', flush=True)
        func_response = "Nothing to do, alarm is not FIRING"

    return response.Response(
        ctx, 
        response_data=func_response,
        headers={"Content-Type": "application/json"}
    )
