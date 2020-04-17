# Function that retrieves an object from a bucket in Object Storage

This function uses Resource Principals to securely authorize a function to make
API calls to OCI services using the [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/index.html).
It returns the content of an object from a bucket in Object Storage.

The function calls the following OCI Python SDK classes:
* [Resource Principals Signer](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/signing.html#resource-principals-signer) to authenticate
* [Object Storage Client](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/object_storage/client/oci.object_storage.ObjectStorageClient.html) to interact with Object Storage

As you make your way through this tutorial, look out for this icon ![user input icon](./images/userinput.png).
Whenever you see it, it's time for you to perform an action.


## Pre-requisites
1. Start by making sure all of your policies are correct from this [guide](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

2. Have [Fn CLI setup with Oracle Functions](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionsconfiguringclient.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Client%20Environment%20for%20Function%20Development%7C_____0)

3. Have your Oracle Object Storage Namespace available. This can be found by
logging into your [cloud account](https://console.us-ashburn-1.oraclecloud.com/),
under your user profile, click on your Tenancy. Your Object Storage Namespace
is shown there.


## Context
Switch to the correct context

![user input icon](./images/userinput.png)
```
fn use context <your context name>
```
Check using
```
fn ls apps
```


## Create or Update your Dynamic Group
In order to use and retrieve information about other OCI Services, your function
must be part of a dynamic group. For information on how to create a dynamic group,
click [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To).

![user input icon](./images/userinput.png)

When specifying the *Matching Rules*, consider the following examples:
* If you want all functions in a compartment to be able to access a resource,
enter a rule similar to the following that adds all functions in the compartment
with the specified compartment OCID to the dynamic group:
```
ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaaaa23______smwa'}
```
* If you want a specific function to be able to access a resource, enter a rule
similar to the following that adds the function with the specified OCID to the
dynamic group:
```
resource.id = 'ocid1.fnfunc.oc1.iad.aaaaaaaaacq______dnya'
```
* If you want all functions with a specific defined tag (free-form tags are
not supported) to be able to access a resource, enter a rule similar to the
following that adds all functions with the defined tag to the dynamic group :
```
ALL {resource.type = 'fnfunc', tag.department.operations.value = '45'}
```


## Create or Update Policies
Now that your dynamic group is created, create a new policy that allows the
dynamic group to read any resources you are interested in receiving
information about, in this case we will grant access to `object-family` in
the functions related compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <your dynamic group name> to read object-family in compartment <your compartment name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to read object-family in compartment demo-func-compartment
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Create an Application to run the function
You can use an application already created or create a new one as follows:

![user input icon](./images/userinput.png)
```
fn create app <app-name> --annotation oracle.com/oci/subnetIds='["<subnet-ocid>"]
```
You can find the subnet-ocid by logging on to [cloud.oracle.com](https://cloud.oracle.com/en_US/sign-in),
navigating to Core Infrastructure > Networking > Virtual Cloud Networks. Make
sure you are in the correct Region and Compartment, click on your VNC and
select the subnet you wish to use.

e.g.
```
fn create app object-crud --annotation oracle.com/oci/subnetIds='["ocid1.subnet.oc1.phx.aaaaaaaacnh..."]'
```

## Review the function
Review the following files in the current folder:
- [requirements.txt](./requirements.txt) specifies all the dependencies for your function
- [func.yaml](./func.yaml) that contains metadata about your function and declares properties
- [func.py](./func.py) which is your actual Python function

The name of your function *oci-objectstorage-get-object* is specified in [func.yaml](./func.yaml).


## Deploy the function
![user input icon](./images/userinput.png)

From the current folder, run the following command:
```
fn -v deploy --app <your app name>
```
e.g.
```
fn -v deploy --app myapp
```


## Invoke the function
![user input icon](./images/userinput.png)
```
echo -n <JSON object> | fn invoke <your app name> <your function name>
```
e.g.
```
echo -n '{"objectName": "<object-name>", "bucketName": "<bucket-name>"}' | fn invoke myapp oci-objectstorage-get-object-python
```
Upon success, you should see the content of the object appear in your terminal.
