# Function that creates a PAR
This function creates a PAR (Pre-Authenticated Request) for a bucket in Object Storage.

As you make your way through this tutorial, look out for this icon ![user input icon](./images/userinput.png).
Whenever you see it, it's time for you to perform an action.

## Pre-requisites
1. Start by making sure all of your policies are correct from this [guide](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

2. Have [Fn CLI setup with Oracle Functions](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionsconfiguringclient.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Client%20Environment%20for%20Function%20Development%7C_____0)

## Create or Update your Dynamic Group
In order to use other OCI Services, your function
must be part of a dynamic group. For information on how to create a dynamic group,
go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To).

![user input icon](./images/userinput.png)

When specifying the *Matching Rules*, consider the following examples:
* Matching all functions in a compartment:
```
ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaaaa23______smwa'}
```
* Matching a specific function by its OCID:
```
resource.id = 'ocid1.fnfunc.oc1.iad.aaaaaaaaacq______dnya'
```
* Matching functions with a defined tag (free-form tags are not supported):
```
ALL {resource.type = 'fnfunc', tag.department.operations.value = '45'}
```

## Create or Update Policies
Create a new policy that allows the dynamic group to manage compute instances. We will grant `manage` access to a specific `bucket` and `objects` in that bucket for a given compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <your dynamic group name> to manage buckets in compartment <your compartment name> where target.bucket.name=<your bucket name>
Allow dynamic-group <your dynamic group name> to manage objects in compartment <your compartment name> where target.bucket.name=<your bucket name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to manage buckets in compartment my-compartment where target.bucket.name='my-bucket'
Allow dynamic-group demo-func-dyn-group to manage objects in compartment my-compartment where target.bucket.name='my-bucket'
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Identify or Create an Application to run your function
You can use an application already created or create a new one as follow:
![user input icon](./images/userinput.png)
```
fn create app <app-name> --annotation oracle.com/oci/subnetIds='["<subnet-ocid>"]'
```
Get the OCID of the subnet in your VCN you wish to use.

e.g.
```
fn create app myapp --annotation oracle.com/oci/subnetIds='["ocid1.subnet.oc1.phx.aaaaaaaacnh..."]'
```

## Review and customize your function
Review:
* the code of the function, [func.py](./func.py)
* its dependencies, [requirements.txt](./requirements.txt)
* the function metadata, [func.yaml](./func.yaml)


## Deploy the function
![user input icon](./images/userinput.png)
```
fn -v deploy --app <your app name>
```
e.g.
```
fn -v deploy --app myapp
```

## Set the function configuration values
The function requires the config value *bucket-name* and *lifetime* to be set.
![user input icon](../images/userinput.png)

Use the *fn* CLI to set the config value:
```
fn config function <your app name> <function name> bucket-name <your bucket name>
fn config function <your app name> <function name> lifetime <PAR lifetime in minutes>
```
e.g.
```
fn config function myapp oci-objectstorage-create-par-python bucket-name 'my-bucket'
fn config function myapp oci-objectstorage-create-par-python lifetime '1'
```

## Invoke the function
![user input icon](./images/userinput.png)
```

echo '{"PAR name": <PAR name> }' | fn invoke <your app name> oci-objectstorage-create-par-python
```
e.g.:
```
echo '{"PAR name": "myPAR" }' | fn invoke myapp oci-objectstorage-create-par-python
```

Upon success, the function returns the PAR URL.