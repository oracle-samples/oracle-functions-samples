# Function that returns the list of compartments in a user's tenancy

This function uses Resource Principals to securely authorize a function to make
API calls to OCI services using the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html).
It returns a list of all compartments within the tenancy. 

The function calls the following OCI Python SDK classes:
* [Resource Principals Signer](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/signing.html#resource-principals-signer) to authenticate
* [Identity Client](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/identity/client/oci.identity.IdentityClient.html) to interact with Identity and Access Management

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


## Create or Update Policies
This function does not require any particular IAM policy.


## Review and customize the function
Review the following files in the current folder:
- [requirements.txt](./requirements.txt) which specifies all the dependencies for your function
- [func.yaml](./func.yaml) which contains metadata about your function and declares properties
- [func.py](./func.py) which is your actual Python function

The name of your function *oci-list-compartments-python* is specified in [func.yaml](./func.yaml).


## Deploy the function

In Cloud Shell, run the `fn deploy` command to build the function and its dependencies as a Docker image, 
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
![user input icon](./images/userinput.png)
```
fn invoke <app-name> <function-name>
```
e.g.
```
fn invoke myapp oci-list-compartments-python
```
You should see all the compartments in your tenancy listed in the terminal.


## Monitoring Functions

Learn how to configure basic observability for your function using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)

