# Function that controls a Compute instance

This function uses Resource Principals to securely authorize a function to make
API calls to OCI services using the [OCI Dotnet SDK](https://docs.oracle.com/iaas/tools/dotnet/latest/api/index.html).
It returns a list of all instances within the compartment that calls the function.

The function calls the following OCI Dotnet SDK classes:
* [ResourcePrincipalAuthenticationDetailsProvider](https://docs.oracle.com/en-us/iaas/tools/dotnet/latest/api/Oci.Common.Auth.ResourcePrincipalAuthenticationDetailsProvider.html) to authenticate
* [ComputeClient](https://docs.oracle.com/en-us/iaas/tools/dotnet/latest/api/Oci.CoreService.ComputeClient.html) to interact with Compute

As you make your way through this tutorial, look out for this icon ![user input icon](./images/userinput.png).
Whenever you see it, it's time for you to perform an action.


## Prerequisites

Before you deploy this sample function, make sure you have run steps A, B 
and C of the [Oracle Functions Quick Start Guide for Cloud Shell](https://www.oracle.com/webfolder/technetwork/tutorials/infographics/oci_functions_cloudshell_quickview/functions_quickview_top/functions_quickview/index.html)
* A - Set up your tenancy
* B - Create application
* C - Set up your Cloud Shell dev environment


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

Create a new policy that allows the dynamic group to `inspect instances` in
the functions related compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <dynamic-group-name> to inspect instances in compartment <compartment-name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to inspect instances in compartment demo-func-compartment
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Review and customize your function

Review the following files in the current folder:
- [ControlInstance.csproj](./ControlInstance.csproj) specifies all the dependencies for your function
- [func.yaml](./func.yaml) that contains metadata about your function and declares properties
- [ControlInstance.cs](./ControlInstance.cs) which contains the Dotnet code

The name of your function *oci-compute-control-dotnet* is specified in [func.yaml](./func.yaml).


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


## Test

Use the *fn* CLI to invoke your function with your app name and the compartment OCID:

![user input icon](./images/userinput.png)
```
echo '{"command":"<command>", "instance_ocid":"<instance-ocid>"}' | fn invoke <app-name> <function-name>
```
e.g.
```
echo '{"command":"stop", "instance_ocid":"ocid1.fnfunc.oc1.iad.aaaaaxxxxx"}' | fn invoke myapp oci-compute-control-dotnet
```
The supported values for command are "status", "start" and "stop".


## Monitoring Functions

Learn how to configure basic observability for your function using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)
