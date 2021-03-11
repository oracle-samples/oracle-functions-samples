## Integrating OCI alerts with Syniverse SMS

OCI monitoring sends an alert when the CPU utilization pass 70%, Oracle Notification Service get this alert and trigger Oracle functions that create a custom message and call Syniverse API to send the SMS.

![workflow](./images/workflow_alert.png)

More
- [Detailed Steps](https://docs.oracle.com/en/learn/events_syniverse/)
- [Syniverse Quick Start](https://sdcsupport.syniverse.com/hc/en-us/articles/236185587-SCG-Quick-Start-guide)


As you make your way through this tutorial, look out for this icon ![user input icon](./images/userinput.png).
Whenever you see it, it's time for you to perform an action.


## Prerequisites

Before you proceed further, ensure you have followed all the steps outlined 
in the parent README file located in [oci-notification-syniverse](../README.md)


## Review and customize the function

Review the following files in the current folder:
* the code of the function, [func.py](./func.py)
* its dependencies, [requirements.txt](./requirements.txt)
* the function metadata, [func.yaml](./func.yaml)


## Deploy the function

In Cloud Shell, run the `fn deploy` command to build *this* function and its dependencies as a Docker image, 
push the image to the specified Docker registry, and deploy *this* function to Oracle Functions 
in the application created earlier:

![user input icon](./images/userinput.png)
```
fn -v deploy --app <app-name>
```
e.g.
```
fn -v deploy --app myapp
```

### Test

In Cloud Shell, run the following `fn invoke` command to unit test this function:

![user input icon](./images/userinput.png)
```
fn invoke <app-name> <function-name> < test-alert.json
```
e.g., 
```
fn invoke myapp oci-alerts-to-syniverse-python < test-alert.json
```

You should see the SMS notifications sent by Syniverse.


## Create a topic and a subscription for the Notification Service

1. From the menu in the upper-left corner, select **Application Integration**, and then select **Notifications**.

2. Click **Create Topic** and create a topic with **Alerts_Syniverse_SMS_Notification** name.

3. Choose your topic, click **Create Subscription** and use the following example:
    * **Protocol**: Function
    * **Function Compartment**: Select the compartment **syniverse_compartment** that you created
    * **Function Application**: myapp
    * **Function**: oci-alerts-to-syniverse-python


## Create an alarm definition

1. From the menu in the upper-left corner, select **Monitoring**, and then select **Alarm definitions**.

2. Click **Create Alarm** and use the following example:
    * **Alarm Name**: 70% CPU Utilization
    * **Alarm severity**: Critical
    * **Alarm body**: OCI Alarm: syniverse. CpuUtilization: 70 

3. On **Metric description** select the compartment **syniverse_compartment**, select **Metric namespace** as oci_computeagent, **Metric name** as CpuUtilization, **Interval** as 1m, and **Statistic** as Max

4. On **Trigger rule** select Value greater than 70

6. On **Notification** select **Destination service** as notification service, select the compartment **syniverse_compartment**, and select **Topic** as Alerts_Syniverse_SMS_Notification


## Monitoring Functions and Notifications Topics

Make sure you configure basic observability for your function and topic using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../../basic-observability/functions.md)
* [Basic Guidance for Monitoring your Notifications Topic](../../basic-observability/notifications.md)

