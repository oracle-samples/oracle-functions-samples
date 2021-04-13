## Convert JSON to CSV

This is a sample to convert JSON to CSV using Service Connector Hub Functions as a Task.

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

In Cloud Shell, run the `fn invoke` ccommand to unit test this function:

![user input icon](./images/userinput.png)
```
fn invoke <app-name> <function-name> < test.json
```
e.g.,
```
fn invoke myapp oci-sch-stream-json-to-csv-python < test.json
```

You should see the the converted CSV output returned by the function.


## Create a Service Connector for reading from Stream 1, convert JSON to CSV and send to Stream 2

1. From the navigation menu, select **Logging**, and then select **Service Connectors**.

2. Click Create Connector, add a Name, Description, select the compartment, select the Source as **Streaming** and Target as **Streaming** and **Functions** as a Task.
    
3. On Configure Source connection, select the compartment, select the your Stream 1.

4. On Configure Target connection, select the compartment, select the your Stream 2. If prompted to create a policy for writing to Streaming, click Create.

5. On Configure Task connection, select the compartment and select the Function. If prompted to create a policy for writing to Functions, click Create.


## Monitoring Functions and Service Connector

Make sure you configure basic observability for your function and connector using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)
* [Basic Guidance for Monitoring your Service Connector](../basic-observability/service-connector-hub.md)
