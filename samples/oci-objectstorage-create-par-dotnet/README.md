# Function that creates a PAR
This function creates a PAR (Pre-Authenticated Request) for a bucket in Object Storage.

As you make your way through this tutorial, look out for this icon ![user input icon](./images/userinput.png).
Whenever you see it, it's time for you to perform an action.


## Prerequisites
Before you deploy this sample function, make sure you have run step A, B and C of the [Oracle Functions Quick Start Guide for Cloud Shell](https://www.oracle.com/webfolder/technetwork/tutorials/infographics/oci_functions_cloudshell_quickview/functions_quickview_top/functions_quickview/index.html)
* A - Set up your tenancy
* B - Create application
* C - Set up your Cloud Shell dev environment


## List Applications 
Assuming your have successfully completed the prerequisites, you should see your 
application in the list of applications.
```
fn ls apps
```


## Create or Update your Dynamic Group
In order to use other OCI Services, your function must be part of a dynamic group. For information on how to create a dynamic group, refer to the [documentation](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To).

When specifying the *Matching Rules*, we suggest matching all functions in a compartment with:
```
ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaxxxxx'}
```
Please check the [Accessing Other Oracle Cloud Infrastructure Resources from Running Functions](https://docs.cloud.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsaccessingociresources.htm) for other *Matching Rules* options.


## Create or Update IAM Policies
Create a new policy that allows the dynamic group to manage compute instances. We will grant `manage` access to a specific `bucket` and `objects` in that bucket for a given compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <dynamic-group-name> to manage buckets in compartment <compartment-name> where target.bucket.name=<bucket-name>
Allow dynamic-group <dynamic-group-name> to manage objects in compartment <compartment-name> where target.bucket.name=<bucket-name>
```
For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Review and customize your function
Review the following files in the current folder:
* the code of the function, [CreatePAR.cs](./CreatePAR.cs)
* its dependencies, [CreatePAR.proj](./CreatePAR.proj)
* the function metadata, [func.yaml](./func.yaml)


## Deploy the function
In Cloud Shell, run the *fn deploy* command to build the function and its dependencies as a Docker image, 
push the image to OCIR, and deploy the function to Oracle Functions in your application.

![user input icon](./images/userinput.png)
```
fn -v deploy --app <app-name>
```


## Set the function configuration values
The function requires the config value *BUCKET_NAME* , *NAMESPACE* , *LIFETIME* and  *REGION* to be set.

![user input icon](./images/userinput.png)

Use the *fn* CLI to set the config value:
```
fn config function <app-name> <function-name> BUCKET_NAME <bucket-name>
fn config function <app-name> <function-name> NAMESPACE <bucket-namespace>
fn config function <app-name> <function-name> LIFETIME <PAR-lifetime-in-minutes>
fn config function <app-name> <function-name> REGION <region>
```
e.g.
```
fn config function myapp oci-objectstorage-create-par-dotnet BUCKET_NAME 'my-bucket'
fn config function myapp oci-objectstorage-create-par-dotnet NAMESPACE 'samplenamespace'
fn config function myapp oci-objectstorage-create-par-dotnet LIFETIME '30'
fn config function myapp oci-objectstorage-create-par-dotnet REGION 'ap-osaka-1'
```

## Invoke the function
The function requires the name of the PAR in the payload to be invoked.

![user input icon](./images/userinput.png)
```

echo '{"PAR name": <PAR name> }' | fn invoke <app-name> oci-objectstorage-create-par-dotnet
```
e.g.:
```
echo '{"PAR name": "myPAR" }' | fn invoke myapp oci-objectstorage-create-par-dotnet
```

Upon success, the function returns the PAR URL.


## Monitoring Functions

Learn how to configure basic observability for your function using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)

