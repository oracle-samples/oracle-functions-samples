# Function that lists objects from a bucket in Object Storage using the OCI Java SDK

This function uses Resource Principals to securely authorize a function to make
API calls to OCI services using the [OCI Java SDK](https://docs.cloud.oracle.com/iaas/tools/java/latest/).
It returns a list of objects from a given bucket in Object Storage.

The function calls the following OCI Java SDK classes:
* [ResourcePrincipalAuthenticationDetailsProvider](https://docs.cloud.oracle.com/en-us/iaas/tools/java/latest/com/oracle/bmc/auth/ResourcePrincipalAuthenticationDetailsProvider.html) to authenticate
* [ObjectStorageClient](https://docs.cloud.oracle.com/iaas/tools/java/latest/com/oracle/bmc/objectstorage/ObjectStorageClient.html) to interact with Object Storage

As you make your way through this tutorial, look out for this icon ![user input icon](../images/userinput.png).
Whenever you see it, it's time for you to perform an action.

## Pre-requisites
1. Start by making sure all of your policies are correct from this [guide](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

2. Have [Fn CLI setup with Oracle Functions](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionsconfiguringclient.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Client%20Environment%20for%20Function%20Development%7C_____0)

3. Have your Oracle Object Storage Namespace available. This can be found by
logging into your [cloud account](https://console.us-ashburn-1.oraclecloud.com/),
under your user profile, click on your Tenancy. Your Object Storage Namespace
is shown there.

## Select Java 11 or Java 8
This folder includes files for both Java 11 and Java 8:
* Java 11 - use [func-jdk11.yaml](func-jdk11.yaml) and
[pom-jdk11.xml](pom-jdk11.xml)
* Java 8 - use [func-jdk8.yaml](func-jdk8.yaml) and
           [pom-jdk8.xml](pom-jdk8.xml)

![user input icon](../images/userinput.png)

Rename `func-jdkXX.yaml` to `func.yaml` and `pom-jdkXX.xml` to `pom.xml`

## Context
Switch to the correct context

![user input icon](../images/userinput.png)
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

![user input icon](../images/userinput.png)

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
dynamic group to inspect any resources you are interested in receiving
information about, in this case we will grant access to `object-family` in
the functions related compartment.

![user input icon](../images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <your dynamic group name> to inspect object-family in compartment <your compartment name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to inspect object-family in compartment demo-func-compartment
```
For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Create an Application to run the function
You can use an application already created or create a new one as follows:

![user input icon](../images/userinput.png)
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
- `pom.xml` specifies all the dependencies for your function
- `func.yaml` that contains metadata about your function and declares properties
- `src/main/java/com/example/fn/ObjectStorageListObjects.java` which contains the Java code

The name of your function *oci-objectstorage-list-objects* is specified in `func.yaml`.

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
echo -n '<bucket_name>' | fn invoke <app_name> oci-objectstorage-list-objects
```
e.g.
```
echo -n 'mybucket' | fn invoke object-crud oci-objectstorage-list-objects
```
Upon success, you should see either a list of objects on your terminal.
