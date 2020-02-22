# Function that returns the list of instances in the calling Compartment.

This function uses Resource Principals to securely authorize a function to make
API calls to OCI services using the [OCI Java SDK](https://docs.cloud.oracle.com/iaas/tools/java/latest/).
It returns a list of all instances within the compartment that calls the function.

The function calls the following OCI Java SDK classes:
* [ResourcePrincipalAuthenticationDetailsProvider](https://docs.cloud.oracle.com/en-us/iaas/tools/java/latest/com/oracle/bmc/auth/ResourcePrincipalAuthenticationDetailsProvider.html) to authenticate
* [ComputeClient](https://docs.cloud.oracle.com/iaas/tools/java/latest/com/oracle/bmc/core/ComputeClient.html) to interact with Compute

As you make your way through this tutorial, look out for this icon ![user input icon](../images/userinput.png).
Whenever you see it, it's time for you to perform an action.


## Pre-requisites
1. Start by making sure all of your policies are correct from this [guide](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

2. Have [Fn CLI setup with Oracle Functions](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionsconfiguringclient.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Client%20Environment%20for%20Function%20Development%7C_____0)


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
information about, in this case we will grant access to `instance-family` in
the functions related compartment.

![user input icon](../images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <your dynamic group name> to inspect instances in compartment <your compartment name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to inspect instances in compartment demo-func-compartment
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Create an Application to run your function
You can use an application already created or create a new one as follow:
![user input icon](../images/userinput.png)
```
fn create app <app-name> --annotation oracle.com/oci/subnetIds='["<subnet-ocid>"]'
```
You can find the subnet-ocid by logging on to [cloud.oracle.com](https://cloud.oracle.com/en_US/sign-in),
navigating to Core Infrastructure > Networking > Virtual Cloud Networks. Make
sure you are in the correct Region and Compartment, click on your VCN and
select the subnet you wish to use.

e.g.
```
fn create app myapp --annotation oracle.com/oci/subnetIds='["ocid1.subnet.oc1.phx.aaaaaaaacnh..."]'
```

## Review and customize your function
Review the following files in the current folder:
- [pom.xml](./pom.xml) specifies all the dependencies for your function
- [func.yaml](./func.yaml) that contains metadata about your function and declares properties
- [src/main/java/com/example/fn/ComputeInstancesList.java](./src/main/java/com/example/fn/ComputeInstancesList.java) which contains the Java code

The name of your function *list-instances* is specified in [func.yaml](./func.yaml).

## Deploy the function
![user input icon](../images/userinput.png)
```
fn -v deploy --app <your app name>
```
e.g.
```
fn -v deploy --app myapp
```


## Invoke the function
Use the *fn* CLI to invoke your function with your app name and the compartment OCID:

![user input icon](../images/userinput.png)
```
echo -n '<COMPARTMENT_OCID>' | fn invoke <your app name> <your function name>
```
e.g.
```
echo -n 'ocid1.compartment.oc1...2jn3htfoobar' | fn invoke myapp list-instances
```
Upon success, you should see a map of instances in your compartment appear on your terminal.
Key is the OCID of the instance and value is a String representation of the Instance object.
