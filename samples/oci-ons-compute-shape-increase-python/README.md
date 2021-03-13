# Automatically Resize VMs
Automatically resize VMs that exceed memory consumption. The function code is referenced in the OCI documentation at https://docs.cloud.oracle.com/en-us/iaas/Content/Notification/Tasks/scenarioa.htm.

This use case involves writing a function to resize VMs and creating an alarm  that sends a message to that function. When the alarm fires, the Notifications service sends the alarm message to the destination topic, which then fans out to the topic's subscriptions. In this scenario, the topic's subscriptions include the function as well as your email. The function is invoked on receipt of the alarm message. 

![ONS to Functions](https://docs.cloud.oracle.com/en-us/iaas/Content/Resources/Images/notifications-scenarioA.png)

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
Create a new policy that allows the dynamic group to *use instances*.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <dynamic-group-name> to use instances in compartment <compartment-name>
```
For more information on how to create policies, check the [documentation](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Review and customize your function
Review the following files in the current folder:
* the code of the function, [func.py](./func.py)
* its dependencies, [requirements.txt](./requirements.txt)
* the function metadata, [func.yaml](./func.yaml)

The following piece of code in [func.py](./func.py) should be updated to match your needs:
```
    if  current_shape == "VM.Standard1.1":
        new_shape = "VM.Standard2.1"
    elif current_shape == "VM.Standard2.1":
        new_shape = "VM.Standard2.2"
```

The code in [list_vm_shapes.py](./list_vm_shapes.py) can be used to improve the logic of VM shape selection.


## Deploy the function
In Cloud Shell, run the fn deploy command to build the function and its dependencies as a Docker image,
push the image to OCIR, and deploy the function to Oracle Functions in your application.

![user input icon](./images/userinput.png)
```
fn -v deploy --app <your app name>
```
e.g.
```
fn -v deploy --app myapp
```


## Configure Oracle Notification Service
This section walks through creating an alarm using the Console and then updating the ONS topic created with the alarm.

![user input icon](./images/userinput.png)

On the OCI console, navigate to *Monitoring* > *Alarm Definitions*. Click *Create Alarm*.

On the Create Alarm page, under Define alarm, set up your threshold: 

Metric description: 
* Compartment: (select the compartment that contains your VM)
* Metric Namespace: oci_computeagent
* Metric Name: MemoryUtilization
* Interval: 1m
* Statistic: Max 

Trigger rule:
* Operator: greater than
* Value: 90  (or lower for testing purposes)
* Trigger Delay Minutes: 1

Select your function under Notifications, Destinations:
* Destination Service: Notifications Service
* Compartment: (select the compartment where you want to create the topic and associated subscriptions)

Topic: Click *Create a topic*
* Topic Name: Alarm Topic
* Subscription Protocol: Function
* Function Compartment: (select the compartment that contains your function)
* Function Application: (select the application that contains your function)
* Function: (select your function)
* Click *Create topic and subscription*

Click Save alarm.


## Test ONS > Fn
First, test the function indivudually.

![user input icon](./images/userinput.png)

Update section "resourceId" in [test-alarm.json](./test-alarm.json) with the OCID of the instance you want to update.

Invoke the function as follows:
```
cat test-alarm.json | fn invoke <your app name> <function name>
```
e.g.:
```
cat test-alarm.json | fn invoke myapp oci-ons-compute-shape-increase-python
```

Now, the whole flow can be tested. Connect to an instance in the compartment where the alarm is active, and stress the memory utilization with the *stress* utility for example.


## Monitoring Functions and Notifications Topics

Learn how to configure basic observability for your function using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)
* [Basic Guidance for Monitoring your Notifications Topics](../basic-observability/notifications.md)

