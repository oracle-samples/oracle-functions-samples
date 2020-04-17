# Function that creates an object in a bucket in Object Storage using the OCI Java SDK

This function uses Resource Principals to securely authorize a function to make
API calls to OCI services using the [OCI Java SDK](https://docs.cloud.oracle.com/iaas/tools/java/latest/).
It creates an object in a bucket in Object Storage and returns a message with a status.

The function calls the following OCI Java SDK classes:
* [ResourcePrincipalAuthenticationDetailsProvider](https://docs.cloud.oracle.com/en-us/iaas/tools/java/latest/com/oracle/bmc/auth/ResourcePrincipalAuthenticationDetailsProvider.html) to authenticate
* [ObjectStorageClient](https://docs.cloud.oracle.com/iaas/tools/java/latest/com/oracle/bmc/objectstorage/ObjectStorageClient.html) to interact with Object Storage

As you make your way through this tutorial, look out for this icon ![user input icon](../images/userinput.png).
Whenever you see it, it's time for you to perform an action.


## Prerequisites
![user input icon](./images/userinput.png)

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
![user input icon](../images/userinput.png)

Assuming your have successfully completed the prerequisites, you should see your 
application in the list of applications.

```
fn ls apps
```


## Create or Update your Dynamic Group
In order to use and retrieve information about other OCI Services, your function
must be part of a dynamic group. For information on how to create a dynamic group,
click [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To).

![user input icon](../images/userinput.png)

When specifying the *Matching Rules*, consider the following example:
* If you want all functions in a compartment to be able to access a resource,
enter a rule similar to the following that adds all functions in the compartment
with the specified compartment OCID to the dynamic group:
```
ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaaaa23______smwa'}
```


## Create or Update Policies
Now that your dynamic group is created, create a new policy that allows the
dynamic group to manage any resources you are interested in updating, in this
case we will grant access to `object-family` in the functions related compartment.

![user input icon](../images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <your dynamic group name> to manage object-family in compartment <your compartment name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to manage object-family in compartment demo-func-compartment
```
For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Review the function
Review the following files in the current folder:
- [pom.xml](./pom.xml) specifies all the dependencies for your function
- [func.yaml](./func.yaml) that contains metadata about your function and declares properties
- [src/main/java/com/example/fn/ObjectStoragePutObject.java](./src/main/java/com/example/fn/ObjectStoragePutObject.java) which contains the Java code

The name of your function *oci-objectstorage-put-object-java* is specified in [func.yaml](./func.yaml).


## Deploy the function
![user input icon](../images/userinput.png)

From the current folder, run the following command:
```
fn -v deploy --app <your app name>
```
e.g.
```
fn -v deploy --app object-crud
```

## Set function configuration values
The function requires the config value *NAMESPACE* to be set.

![user input icon](../images/userinput.png)

Use the *fn* CLI to set the config value:
```
fn config function <your app name> <function name> NAMESPACE <your namespace>
```
e.g.
```
fn config function object-crud list-objects NAMESPACE mytenancy
```
Note that the config value can also be set at the application level:
```
fn config app <your app name> NAMESPACE <your namespace>
```
e.g.
```
fn config app object-crud NAMESPACE mytenancy
```


## Invoke the function
Use the *fn* CLI to invoke your function with your own bucket name and app name:

![user input icon](../images/userinput.png)
```
echo -n '{"name": "<object_name>", "bucketName":"<bucket_name>", "content": "<text_content>"}' | fn invoke <app_name> <function_name>
```
e.g.
```
echo -n '{"name": "file1.txt", "bucketName":"test", "content": "This file was created in OCI object storage bucket using Oracle Functions"}' | fn invoke object-crud oci-objectstorage-put-object-java
```
Upon success, you should see a success message appear in your terminal.
