#
# oci-compute-control-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import oci

from fdk import response

def instance_status(compute_client, instance_id):
    return compute_client.get_instance(instance_id).data.lifecycle_state

def instance_start(compute_client, instance_id):
    print('Starting Instance: {}'.format(instance_id))
    try:
        if instance_status(compute_client, instance_id) in 'STOPPED':
            try:
                resp = compute_client.instance_action(instance_id, 'START')
                print('Start response code: {0}'.format(resp.status))
            except oci.exceptions.ServiceError as e:
                print('Starting instance failed. {0}' .format(e))
                raise
        else:
            print('The instance was in the incorrect state to start' .format(instance_id))
            raise
    except oci.exceptions.ServiceError as e:
        print('Starting instance failed. {0}'.format(e))
        raise
    print('Started Instance: {}'.format(instance_id))
    return instance_status(compute_client, instance_id)

def instance_stop(compute_client, instance_id):
    print('Stopping Instance: {}'.format(instance_id))
    try:
        if instance_status(compute_client, instance_id) in 'RUNNING':
            try:
                resp = compute_client.instance_action(instance_id, 'STOP')
                print('Stop response code: {0}'.format(resp.status))
            except oci.exceptions.ServiceError as e:
                print('Stopping instance failed. {0}' .format(e))
                raise
        else:
            print('The instance was in the incorrect state to stop' .format(instance_id))
            raise
    except oci.exceptions.ServiceError as e:
        print('Stopping instance failed. {0}'.format(e))
        raise
    print('Stopped Instance: {}'.format(instance_id))
    return instance_status(compute_client, instance_id)

def handler(ctx, data: io.BytesIO=None):
    try:
        body = json.loads(data.getvalue())
        instance_ocid = body.get("instance_ocid")
        command = body.get("command")
    except (Exception) as ex:
        print("Two arguments need to be passed to the function, instance_ocid and the command")
        print(str(ex), flush=True)
        raise

    signer = oci.auth.signers.get_resource_principals_signer()
    compute_client = oci.core.ComputeClient(config={}, signer=signer)

    if command == 'status':
        resp = instance_status(compute_client, instance_ocid)
    elif command == 'start':
        resp = instance_start(compute_client, instance_ocid)
    elif command == 'stop':
        resp = instance_stop(compute_client, instance_ocid)
    else:
        print("command not supported", flush=True)
        raise

    return response.Response(
        ctx, 
        response_data=json.dumps({"status": "{0}".format(resp)}),
        headers={"Content-Type": "application/json"}
    )
