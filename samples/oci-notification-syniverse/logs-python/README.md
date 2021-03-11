## Integrating OCI Logs with Syniverse SMS

Service Connector Hub will read the logs and trigger Oracle Functions that create a custom message and call Syniverse API to send the SMS.

![workflow](./images/workflow_log.png)

More
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
e.g.,
```
fn -v deploy --app myapp
```

### Test

In Cloud Shell, run the following `fn invoke` command to unit test this function:

![user input icon](./images/userinput.png)
```
fn invoke <app-name> <function-name> < test-logs.json
```
e.g., 
```
fn invoke myapp oci-logs-to-syniverse-python < test-logs.json
```

You should see the SMS notifications sent by Syniverse.


## Configure the logs you want to capture

1. From the [OCI Console](https://cloud.oracle.com) navigation menu, select **Logging**, and then select **Log Groups**.

2. Click Create Log Group, select your compartment, add a Name and Description

3. Select Logs in the left menu, click Enable Service Log, select your compartment, select Log Category on Service and fill the rest of the fields appropriately.


## Create a Service Connector to get logs from OCI Logging and send to the Function

1. From the navigation menu, select **Logging**, and then select **Service Connectors**.

2. Click Create Connector, add a Name, Description, select the compartment, select the source as **Logging** and Target as **Functions**.
    
3. On Configure Source connection, select the compartment, select the Log Group created earlier

4. On Configure Target connection, select the compartment and select the Function name. If prompted to create a policy for writing to Function, click Create.


## Monitoring Functions and Service Connector

Make sure you configure basic observability for your function and connector using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)
* [Basic Guidance for Monitoring your Service Connector](../basic-observability/service-connector-hub.md)


