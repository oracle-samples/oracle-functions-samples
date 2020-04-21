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
| Invoke another Function                              |[sample](./oci-invoke-function-python)| |
| Run a SQL statement against Autonomous DB using ORDS | [sample](./oci-adb-ords-runsql-python) | 
| Run a SQL statement against Autonomous DB using DB Client |[sample](./oci-adb-client-runsql-python)|| 
| Publish a notification using ONS                     |[sample](./oci-ons-publish-python)|
| Send an email using Email Delivery Service           |[sample](./oci-email-send-python)|
| Decrypt cipher using Vault keys                      |[sample](./oci-vault-decrypt-python)

## Use Cases
| Description                                          | Code | Docs |
|------------------------------------------------------|:------:|:----:|
| Provide the size of an image (Custom Dockerfile, image library) | [repo](./imagedims-python)|
| Automatically load data from Object Storage into Autonomous DataWarehouse | [repo](./oci-load-file-into-adw-python)|

## Documentation

You can find the online documentation for Oracle Functions at [docs.oracle.com](https://docs.cloud.oracle.com/iaas/Content/Functions/Concepts/functionsoverview.htm) and information about the Fn project at [https://fnproject.io/](https://fnproject.io/).

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md)

## License

See [LICENSE](./LICENSE.txt)
