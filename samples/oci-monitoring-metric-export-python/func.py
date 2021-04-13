#
# oci-monitoring-metric-export-python version 1.0.
#
# Copyright (c) 2021 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#


import io
import oci
import requests
import logging
import json
from datetime import datetime, timedelta
from fdk import response



"""
Create Object Storage bucket 'metrics-export' in the specified Compartent, if it does not already exist.
Default access:  Private
"""
def createBucketIfNotExists(_source_namespace, _compartmentId, _bucketname, _object_storage_client, logger):
    try:
        LiveBucketList = set()
        LiveBucketResponse = _object_storage_client.list_buckets(_source_namespace, _compartmentId)
        for bucket in LiveBucketResponse.data:
            LiveBucketList.add(bucket.name)
        if _bucketname not in LiveBucketList:
            request = oci.object_storage.models.CreateBucketDetails()
            request.compartment_id = _compartmentId
            request.name = _bucketname
            bucket = _object_storage_client.create_bucket(_source_namespace, request) 
    except Exception as e:
        logger.error("Error in createBucketIfNotExists(): {}".format(str(e)))
        raise

"""
Delete target objectname if it already exists.  
Due to filenames containing embedded timestamps this scenario is rare, but could occur if re-executing a previous export with specific start/end timestamps.
"""
def deleteObjectIfExists(_source_namespace, _bucketname, _objectname, _object_storage_client, logger):
    liveObjects = set()
    try:
        response = _object_storage_client.list_objects(namespace_name=_source_namespace, delimiter='/', bucket_name=_bucketname, fields='name,timeCreated,size')
        for obj in response.data.objects:
            if (obj.name == _objectname):
                _object_storage_client.delete_object(_source_namespace, _bucketname, _objectname)
    except Exception as e:
        logger.error("Error in deleteObjectIfExists(): {}".format(str(e)))
        raise

"""
Perform api call to pull metrics
"""
def export_metrics(monitoring_client, _compartmentId, _namespace, _resource_group, _query, _startdtm, _enddtm, _resolution, logger):        
    try:
        _dataDetails = oci.monitoring.models.SummarizeMetricsDataDetails ()
        _dataDetails.namespace=_namespace
        _dataDetails.query=_query
        if (_resource_group.strip() != ""):
            _dataDetails.resource_group=_resource_group
        _dataDetails.start_time=_startdtm
        _dataDetails.end_time=_enddtm
        _dataDetails.resolution=_resolution
        
        print(_resource_group)
        print(_dataDetails)

        summarize_metrics_data_response = monitoring_client.summarize_metrics_data (
            compartment_id=_compartmentId, summarize_metrics_data_details =_dataDetails)
        return summarize_metrics_data_response.data
    except Exception as e:
        logger.error("Error in export_metrics(): {}".format(str(e)))
        raise
"""
Upload (put) metrics json file to bucket 'metrics-export'
"""
def putObject(_source_namespace, _bucketname, _objectname, _content, _object_storage_client, logger):
    try:
        put_object_response = _object_storage_client.put_object(_source_namespace, _bucketname, _objectname, _content)
    except Exception as e:
        logger.error("Error in putObject(): {}".format(str(e)))
        raise


"""
Entrypoint and initialization
"""
def handler(ctx, data: io.BytesIO=None):
    logger = logging.getLogger()
    logger.info("function start")
    signer = oci.auth.signers.get_resource_principals_signer()
    configinfo = {'region': signer.region, 'tenancy': signer.tenancy_id}
    monitoring_client = oci.monitoring.MonitoringClient(config={}, signer=signer)
    object_storage_client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    source_namespace = object_storage_client.get_namespace(retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY).data
    
    # Retrieve the Function configuration values
    # Parse input parameters and assign default values as needed
    try:
        cfg = dict(ctx.Config())
        try:
            _compartmentId = cfg["compartmentId"]
        except Exception as e:
            logger.error('Mandatory key compartmentId not defined')
            raise

        try:
            _namespace = cfg["namespace"]
        except:
            logger.info('Optional configuration key namespace unavailable.  Will assign default value')
            _namespace = "oci_computeagent"                    

        try:
            _resource_group = cfg["resource_group"]
        except:
            logger.info('Optional configuration key resource_group unavailable.  Will assign default value') 
            _resource_group = ""       

        try:    
            _query = cfg["query"]
        except:
            logger.info('Optional configuration key query unavailable.  Will assign default value')
            _query = "CpuUtilization[1m].mean()"

        try:    
            _startdtm = cfg["startdtm"]
        except:
            logger.info('Optional configuration key startdtm unavailable.  Will assign default value')        
            _startdtm = (datetime.now() + timedelta(hours=-1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        try:
            _enddtm = cfg["enddtm"]
        except:
            logger.info('Optional configuration key enddtm unavailable.  Will assign default value')
            _enddtm = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        try:
            _resolution = cfg["resolution"]
        except:
            logger.info('Optional configuration key resolution unavailable.  Will assign default value')
            _resolution = "1m"
    

        bucketname = "metrics-export"
        dt_string =  _enddtm

        if (_resource_group.strip()):
            objectname = _namespace + "-" + _resource_group + "-" + dt_string[0:19]  + ".json"
        else:
            objectname = _namespace + "-" + dt_string[0:19] + ".json"

        logger.info("compartmentId: {}".format(str(_compartmentId)))
        logger.info("namespace: {}".format(str(_namespace)))
        logger.info("resource_group: {}".format(str(_resource_group)))
        logger.info("query: {}".format(str(_query)))
        logger.info("startdtm: {}".format(str(_startdtm)))
        logger.info("enddtm: {}".format(str(_enddtm)))
        logger.info("resolution: {}".format(str(_resolution)))
        logger.info("source_namespace: {}".format(str(source_namespace)))

    except Exception as e:
        logger.error("Error in retrieving and assigning configuration values")
        raise
        
    # Main tasks
    try:    
        createBucketIfNotExists(source_namespace, _compartmentId, bucketname, object_storage_client, logger)
        deleteObjectIfExists(source_namespace, bucketname, objectname, object_storage_client, logger)
        listContent = export_metrics(monitoring_client, _compartmentId, _namespace, _resource_group, _query, _startdtm, _enddtm, _resolution, logger)
        putObject(source_namespace, bucketname, objectname, str(listContent), object_storage_client, logger)
    except Exception as e:
        logger.error("Error in main process: {}".format(str(e)))
        raise
    
    # The function is complete, return info tbd
    logger.info("function end")
    return response.Response(
        ctx, 
        response_data="",
        headers={"Content-Type": "application/json"}
    )