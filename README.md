# Oracle Functions Samples

![Oracle Functions logo](./images/FunctionsLogo_16x16.png)

This repository provides examples demonstrating how to use Oracle Functions.

## Setup
* [Quick start](https://www.oracle.com/webfolder/technetwork/tutorials/infographics/oci_faas_gettingstarted_quickview/functions_quickview_top/functions_quickview/index.html)

## How To
| Description                                          | Python | Java | 
|------------------------------------------------------|:------:|:----:|
| Hello World                                          |[sample](./helloworld)|[sample](./helloworld)|
| List OCI Compute instances                           |[sample](./oci-list-instances-python)|[sample](./oci-list-instances-java)|
| Control OCI Compute instances (start/stop/status)    |[sample](./oci-compute-control-python)|
| List OCI compartments                                |[sample](./oci-list-compartments-python)|
| List objects in OCI Object Storage                   |[sample](./oci-objectstorage-list-objects-python)|[sample](./oci-objectstorage-list-objects-java)|
| Read an object in OCI Object Storage                 |[sample](./oci-objectstorage-get-object-python)|[sample](./oci-objectstorage-get-object-java)|
| Create an object in OCI Object Storage               |[sample](./oci-objectstorage-put-object-python)|[sample](./oci-objectstorage-put-object-java)|
| Create a PAR in OCI Object Storage                   |[sample](./oci-objectstorage-create-par-python)||
| Display an OCI Cloud Event                           |[sample](./oci-event-display-python)|
| Invoke another Function                              |[sample](./oci-invoke-function-python)|[sample](./oci-invoke-function-byid-java)||
| Run a SQL statement against Autonomous DB using ORDS | [sample](./oci-adb-ords-runsql-python) | 
| Run a SQL statement against Autonomous DB using DB Client |[sample](./oci-adb-client-runsql-python)|| 
| Run a SQL statement against Autonomous DB using JDBC ||[sample](./oci-adb-jdbc-java)|
| Publish a notification using ONS                     |[sample](./oci-ons-publish-python)|
| Send an email using Email Delivery Service           |[sample](./oci-email-send-python)|
| Decrypt cipher using Vault keys                      |[sample](./oci-vault-decrypt-python)
| Get a secret from Vault                              |[sample](./oci-vault-get-secret-python)|
| API Gateway Function authorizer for IDCS             | |[sample](./oci-apigw-authorizer-idcs-java)
| Function that returns the API Gateway HTTP request information |[sample](./oci-apigw-display-httprequest-info-python)
| Function for API Gateway that validates an API key   |[sample](./oci-apigw-apikey-validation-python)

## Use Cases
| Description                                          | Code | Docs |
|------------------------------------------------------|:------:|:----:|
| Provide the size of an image (Custom Dockerfile, image library) | [repo](./imagedims-python)|
| Automatically load data from Object Storage into Autonomous DataWarehouse | [repo](./oci-load-file-into-adw-python)|
| Automatically resize VM on High Memory Alerts (Notifications trigger a function) | [repo](./oci-ons-compute-shape-increase-python)|
| Check if a compute instance is tagged correctly on provisioning, if not, stop it | [repo](./oci-stop-untagged-instance-python)|

## Community-led Examples
| Description                                          | Code | Blog |
|------------------------------------------------------|:------:|:----:|
| Serverless SaaS Extensions using Oracle Functions, API Gateway and VBCS |  | [blog](https://www.ateam-oracle.com/the-cloud-native-approach-to-extending-your-saas-applications)
| Function that demonstrates connectivity between Oracle SaaS applications with OIC | [repo](./oci-oic-hsm-object-upload)|


## Documentation

You can find the online documentation for Oracle Functions at [docs.oracle.com](https://docs.cloud.oracle.com/iaas/Content/Functions/Concepts/functionsoverview.htm) and information about the Fn project at [https://fnproject.io/](https://fnproject.io/).

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md)

## License

See [LICENSE](./LICENSE.txt)
