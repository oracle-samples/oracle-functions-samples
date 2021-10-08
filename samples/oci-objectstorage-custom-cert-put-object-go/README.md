# Function that creates an object in a bucket in Object Storage using the OCI Java SDK with custom certificate

This function uses Resource Principals to securely authorize a function to make
API calls to OCI services using the [OCI Go SDK](hhttps://docs.oracle.com/en-us/iaas/tools/go/46.1.0/).
It creates an object in a bucket in Object Storage and returns a message with a status.

Some OCI realms uses self signed certificates. Certificate being used can be specified in client we create
in function to connect to OCI services. In this function, certificate to be trusted is specified in the client we are creating to interact with Object Storage. 

The function calls the following OCI Go SDK classes:
* [ResourcePrincipalConfigurationProvider](https://docs.oracle.com/en-us/iaas/tools/go/47.1.0/common/auth/index.html#ResourcePrincipalConfigurationProvider) to authenticate
* [NewObjectStorageClientWithConfigurationProvider](https://docs.oracle.com/en-us/iaas/tools/go/47.1.0/objectstorage/index.html#NewObjectStorageClientWithConfigurationProvider) to interact with Object Storage

As you make your way through this tutorial, look out for this icon ![user input icon](./images/userinput.png).
Whenever you see it, it's time for you to perform an action.


## Prerequisites

1. Before you deploy this sample function, make sure you have run steps A, B 
and C of the [Oracle Functions Quick Start Guide for Cloud Shell](https://www.oracle.com/webfolder/technetwork/tutorials/infographics/oci_functions_cloudshell_quickview/functions_quickview_top/functions_quickview/index.html)
    * A - Set up your tenancy
    * B - Create application
    * C - Set up your Cloud Shell dev environment

2. Have your Oracle Object Storage Namespace available. This can be found by
logging into your [cloud account](https://console.us-ashburn-1.oraclecloud.com/),
under your user profile, click on your Tenancy. Your Object Storage Namespace
is shown there.


## List Applications 

Assuming you have successfully completed the prerequisites, you should see your 
application in the list of applications.

```
fn ls apps
```


## Create or Update your Dynamic Group

In order to use other OCI Services, your function must be part of a dynamic 
group. For information on how to create a dynamic group, refer to the 
[documentation](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To).

When specifying the *Matching Rules*, we suggest matching all functions in a compartment with:

```
ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaxxxxx'}
```


## Create or Update IAM Policies
Create a new policy that allows the dynamic group to `manage objects` in 
the functions related compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <dynamic-group-name> to manage objects in compartment <compartment-name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to manage objects in compartment demo-func-compartment
```
For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Review and customize the function

Review the following files in the current folder:
- [go.mod](./go.mod) specifies all the dependencies for your function
- [func.yaml](./func.yaml) that contains metadata about your function and declares properties
- [func.go](./func.go) which contains the go code

The name of your function is specified in [func.yaml](./func.yaml).


## Deploy the function

In Cloud Shell, run the *fn deploy* command to build the function and its dependencies as a Docker image, 
push the image to the specified Docker registry, and deploy the function to Oracle Functions 
in the application created earlier:

![user input icon](./images/userinput.png)

```
fn -v deploy --app <app-name>
```
e.g.
```
fn -v deploy --app myapp
```

## Create a bucket called "test"

![user input icon](./images/userinput.png)

From the OCI Console > Core Infrastructure > Object Storage > Create Bucket with bucket name = "test"

## Test

Use the *fn* CLI to invoke your function with your own bucket name and app name:

![user input icon](./images/userinput.png)
```
echo -n '{"name": "<object-name>", "bucketName":"<bucket-name>", "content": "<text-content>"}' | fn invoke <app-name> <function-name>
```
e.g.
```
echo -n '{"name": "file1.txt", "bucketName":"mybucket", "content": "This file was created in OCI object storage bucket using Oracle Functions"}' | fn invoke myapp oci-objectstorage-custom-cert-put-object-go
```
You should see a success message appear in your terminal.


## Monitoring Functions

Learn how to configure basic observability for your function using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)

