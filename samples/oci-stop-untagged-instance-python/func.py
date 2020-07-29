#
# oci-stop-untagged-instance-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
from fdk import response

import oci

def handler(ctx, data: io.BytesIO=None):

    resp=None

    try:
      body = json.loads(data.getvalue())  
      jsondata = body.get("data")


      print("event type          : " + body["eventType"],flush=True)
      print("Instance Id         : " + body["data"]["resourceId"],flush=True)
      print("Instance Name       : " + body["data"]["resourceName"],flush=True)
      print("Availability Domain : " + body["data"]["availabilityDomain"],flush=True)

      print(jsondata.get("resourceId"),flush=True)
      print(jsondata.get("resourceName"),flush=True)
      print(jsondata.get("availabilityDomain"),flush=True)
     
      print(json.dumps(body, indent=4), flush=True)

      instanceId = body["data"]["resourceId"]
      signer = oci.auth.signers.get_resource_principals_signer()
    
      resp   = do(signer,instanceId)

      return response.Response(
        ctx, response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
      )
    except ( Exception, ValueError) as e:
      print("Error " +  str(e), flush=True)

def do(signer,instanceId):

    print("Searching for untagged instance", flush=True)

    results = ""
    message = ""
    resp    = ""

    try:
        search_client = oci.resource_search.ResourceSearchClient(config={}, signer=signer)
        print("Search client initialized",flush=True)

        key="costcenter"
        value="1234"

        structured_search = oci.resource_search.models.StructuredSearchDetails(
                query="query instance resources where ((freeformTags.key != '{}' && freeformTags.value != '{}') && (identifier='{}'))".format(key,value,instanceId),
                type='Structured',
                matching_context_type=oci.resource_search.models.SearchDetails.MATCHING_CONTEXT_TYPE_NONE)
        results = search_client.search_resources(structured_search)
        if len(results.data.items) == 1:
           message = "Instance " + instanceId + " was untagged "
           print(message, flush=True)
           resp = perform_action(signer,instanceId, 'STOP')
        else:
           message = "Instance " + instanceId + " properly tagged "
           print(message, flush=True)
     
    except oci.exceptions.ServiceError as e:
            print('RQS Search failed with Service Error: {0}'.format(e),flush=True)
            raise
    except oci.exceptions.RequestException as e:
            print('RQS Search failed w/ a Request exception. {0}'.format(e),flush=True)
            raise

    return resp


def perform_action(signer,instanceId,action):
    
    compute_client = oci.core.ComputeClient(config={}, signer=signer)
    print("Performing action", flush=True)
    try:
        if compute_client.get_instance(instanceId).data.lifecycle_state in ('RUNNING'):
            try:

                 resp = compute_client.instance_action(instanceId,action)
                 print('response code: {0}'.format(resp.status),flush=True)
            except oci.exceptions.ServiceError as e:
                print('Action failed. {0}'.format(e),flush=True)
                raise
        else:
            print('The instance {0} was in the incorrect state to stop'.format(instanceId),flush=True)
    except oci.exceptions.ServiceError as e:
        print('Action failed. {0}'.format(e),flush=True)
        raise

    print('Action ' + action + ' performed on instance: {}'.format(instanceId),flush=True)

    return compute_client.get_instance(instanceId).data.lifecycle_state
