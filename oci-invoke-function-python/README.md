# Function that invoke another function

This function invokes another function.

As you make your way through this tutorial, look out for this icon ![user input icon](./images/userinput.png).
Whenever you see it, it's time for you to perform an action.

## Pre-requisites
1. Start by making sure all of your policies are correct from this [guide](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

2. Have [Fn CLI setup with Oracle Functions](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionsconfiguringclient.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Client%20Environment%20for%20Function%20Development%7C_____0)


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
dynamic group to read any resources you are interested in receiving
information about, in this case we will grant access to `functions-family` in
the functions related compartment.

![user input icon](../images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <your dynamic group name> to use functions-family in compartment <your compartment name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to use functions-family in compartment demo-func-compartment
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Create an Application to run your function
You can use an application already created or create a new one as follow:
![user input icon](./images/userinput.png)
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


## Invoke the function
![user input icon](./images/userinput.png)
Create another function such as a HelloWorld function ([HelloWorld Sample](../../helloworld))