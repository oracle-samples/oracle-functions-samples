# Oracle Functions Samples

![Oracle Functions logo](./images/FunctionsLogo_16x16.png)

This repository provides examples demonstrating how to use Oracle Functions.

## Setup
* [Quick start](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartguidestop.htm)

## Basic Observability Guidance
* [Functions](./samples/basic-observability/functions.md)
* [Service Connector Hub](./samples/basic-observability/service-connector-hub.md)
* [Notifications Service](./samples/basic-observability/notifications.md)

## How To
| Description                                          | Python | Java | 
|------------------------------------------------------|:------:|:----:|
| Hello World                                          |[sample](./samples/helloworld)|[sample](./samples/helloworld)|
| List OCI Compute instances                           |[sample](./samples/oci-list-instances-python)|[sample](./samples/oci-list-instances-java)|
| Control OCI Compute instances (start/stop/status)    |[sample](./samples/oci-compute-control-python)|
| List OCI compartments                                |[sample](./samples/oci-list-compartments-python)|
| List objects in OCI Object Storage                   |[sample](./samples/oci-objectstorage-list-objects-python)|[sample](./samples/oci-objectstorage-list-objects-java)|
| Read an object in OCI Object Storage                 |[sample](./samples/oci-objectstorage-get-object-python)|[sample](./samples/oci-objectstorage-get-object-java)|
| Create an object in OCI Object Storage               |[sample](./samples/oci-objectstorage-put-object-python)|[sample](./samples/oci-objectstorage-put-object-java)|
| Create a PAR in OCI Object Storage                   |[sample](./samples/oci-objectstorage-create-par-python)||
| Display an OCI Cloud Event                           |[sample](./samples/oci-event-display-python)|
| Invoke another Function using the OCI SDK            |[sample](./samples/oci-invoke-function-python)|||
| Run a SQL statement against Autonomous DB using ORDS | [sample](./samples/oci-adb-ords-runsql-python) | 
| Run a SQL statement against Autonomous DB using DB Client |[sample](./samples/oci-adb-client-runsql-python)|| 
| Publish a notification using ONS                     |[sample](./samples/oci-ons-publish-python)|
| Send an email using Email Delivery Service           |[sample](./samples/oci-email-send-python)|
| Decrypt cipher using Vault keys                      |[sample](./samples/oci-vault-decrypt-python)
| Get a secret from Vault                              |[sample](./samples/oci-vault-get-secret-python)|
| Write IAM policies that enables Functions in a tenancy to access resources in other tenancies ||[sample](./samples/oci-cross-tenancy-policies-java)
| Trace a function with APM and add custom child spans using Zipkin |[sample](./samples/trace-functions-with-apm)|

## Functions and API Gateway
[Oracle Cloud Functions](https://www.oracle.com/cloud-native/functions/) and [OCI API Gateway](https://www.oracle.com/api) together enable developers to create serverless APIs and perform function based authorization.
| Description                                          | Python | Java | 
|------------------------------------------------------|:------:|:----:|
| API Gateway Function authorizer for IDCS             | |[sample](./samples/oci-apigw-authorizer-idcs-java) |
| Function that returns the API Gateway HTTP request information for testing | [sample](./samples/oci-apigw-display-httprequest-info-python) | |
| Validate an API key   |[sample](./samples/oci-apigw-apikey-validation-python) | |
| BasicAuth Validation with IDCS | |[sample](./samples/oci-apigw-idcs-auth-basic) |


## Using Service Connector Hub with Functions
| Description                                          | Code |
|------------------------------------------------------|:------:|
| _**Logging >> Service Connector Hub >> Functions**_ | |
| Move logs from OCI to Datadog using Service Connector Hub, Logging (Source), Functions (Target) and Datadog | [sample](./samples/oci-logs-datadog) |
| Send SMS messages for logs using Service Connector Hub, Logging (Source), Functions (Target) and Syniverse SMS | [sample](./samples/oci-notification-syniverse) |
| | |
| _**Streaming >> Service Connector Hub >> Functions**_ | |
| Convert JSON to CSV format using Service Connector Hub, Streams (Source and Target) and Functions (Task) | [sample](./samples/oci-serviceconnector-streaming-json-to-csv-python) |
| Convert JSON to Parquet format using Service Connector Hub, Streams (Source and Target) and Functions (Task) | [sample](./samples/oci-serviceconnector-streaming-json-to-parquet-python) |


## Other Use Cases
| Description                                          | Code |
|------------------------------------------------------|:------:|
| Provide the size of an image (Custom Dockerfile, image library) | [sample](./samples/imagedims-python) |
| Automatically load data from Object Storage into Autonomous DataWarehouse | [sample](./samples/oci-load-file-into-adw-python) |
| Automatically resize VM on High Memory Alerts (Notifications trigger a function) | [sample](./samples/oci-ons-compute-shape-increase-python) |
| Check if a compute instance is tagged correctly on provisioning, if not, stop it | [sample](./samples/oci-stop-untagged-instance-python) |
| Send SMS messages for monitoring alarms using Monitoring, Notifications Service, Functions and Syniverse SMS | [sample](./samples/oci-notification-syniverse) |
| Export a collection of historical metrics from Monitoring Service using the Monitoring Query Language (MQL)  | [sample](./samples/oci-monitoring-metric-export-python) |


## Community-led Examples
| Description                                          | Code | Blog |
|------------------------------------------------------|:------:|:----:|
| Serverless SaaS Extensions using Oracle Functions, API Gateway and VBCS | [repo](https://github.com/oracle/cloud-asset-fusion-serverless-vbcs-sample) | [blog](https://www.ateam-oracle.com/the-cloud-native-approach-to-extending-your-saas-applications)
| Function that demonstrates connectivity between Oracle SaaS applications with OIC | [sample](./samples/oci-oic-hcm-object-upload)|

## Documentation

You can find the online documentation for Oracle Functions at [docs.oracle.com](https://docs.cloud.oracle.com/iaas/Content/Functions/Concepts/functionsoverview.htm) and information about the Fn project at [https://fnproject.io/](https://fnproject.io/).

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md)

## License

See [LICENSE](./LICENSE.txt)
