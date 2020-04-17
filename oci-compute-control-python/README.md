# Function that controls a Compute instance

This function starts, stops and return the status of an OCI Compute instance.

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

Create a new policy that allows the dynamic group to manage compute instances. 
We will grant `manage` access to `instances` in the compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <dynamic-group-name> to manage instances in compartment <compartment-name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to manage instances in compartment demo-func-compartment
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Review and customize the function

Review the following files in the current folder:
* the code of the function, [func.py](./func.py)
* its dependencies, [requirements.txt](./requirements.txt)
* the function metadata, [func.yaml](./func.yaml)


## Deploy the function

![user input icon](./images/userinput.png)
```
fn -v deploy --app <app-name>
```
e.g.
```
fn -v deploy --app myapp
```

### Invoke the function

In Cloud Shell, run the `fn deploy` command to build the function and its dependencies as a Docker image, 
push the image to the specified Docker registry, and deploy the function to Oracle Functions 
in the application created earlier:

![user input icon](./images/userinput.png)
```
echo '{"command":"<command>", "instance_ocid":"<instance-ocid>"}' | fn invoke <app-name> <function-name>
```
e.g. To stop an instance:
```
echo '{"command":"stop", "instance_ocid":"ocid1.fnfunc.oc1.iad.aaaaaxxxxx"}' | fn invoke myapp oci-compute-control-python
```
The supported values for `command` are "status", "start" and "stop".


You should see the status of the instance returned by the function.
