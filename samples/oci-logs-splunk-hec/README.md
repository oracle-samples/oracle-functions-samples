## Monitor Oracle Cloud Infrastructure Logs with Splunk

Forward logs from Oracle Cloud Infrastructure Logging service to Splunk via
HTTP Event Connector


![workflow](./images/workflow.png)


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


## Configure your Function

In order to send logs to Splunk you'll need to define two environment variables:
* `SPLUNK_HEC_ENDPOINT` - the HTTP/HTTPS REST endpoint for the HEC service
* `SPLUNK_HEC_TOKEN` - the Token used to authenticate


### Splunk Enterprise / Splunk Cloud

If you haven't already you'll need to set up the HTTP Event Collector service
on your Splunk Instance. Instructions on configuring and using the HEC are
available at https://docs.splunk.com/Documentation/Splunk/9.0.1/Data/UsetheHTTPEventCollector.


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


## Configure the logs you want to capture

1. From the [OCI Console](https://cloud.oracle.com) navigation menu, select **Logging**, and then select **Log Groups**.

2. Click Create Log Group, select your compartment, add a Name and Description

3. Select Logs in the left menu, click Enable Service Log, select your compartment, select Log Category on Service and fill the rest of the fields appropriately.


## Create a Service Connector for reading logs from Logging and send to Functions

1. From the navigation menu, select **Logging**, and then select **Service Connectors**.

2. Click Create Connector, add a Name, Description, select the compartment, select the Source as **Logging** and Target as **Functions**.

3. On Configure Source connection, select the compartment, select the Log Group created earlier.

4. On Configure Target connection, select the compartment and select the Function. If prompted to create a policy for writing to functions, click Create.


## Monitoring Functions and Service Connector

Make sure you configure basic observability for your function and connector using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)
* [Basic Guidance for Monitoring your Service Connector](../basic-observability/service-connector-hub.md)

---
## Function Environment

Here are the supported Function parameters:

| Environment Variable        | Default           | Purpose  |
| ------------- |:-------------:| :----- |
| SPLUNK_HEC_ENDPOINT      | not-configured | REST API endpoint for reaching Splunk HEC ([see docs](https://docs.splunk.com/Documentation/Splunk/9.2.0/Data/UsetheHTTPEventCollector#Configure_HTTP_Event_Collector_on_Splunk_Cloud_Platform))|
| SPLUNK_HEC_TOKEN      	| not-configured      |   HEC authentication token obtained from Splunk HEC configuration |
| LOGGING_LEVEL | INFO     |    Controls function logging outputs.  Choices: INFO, WARN, CRITICAL, ERROR, DEBUG |

---
## License
Copyright (c) 2024, Oracle and/or its affiliates. All rights reserved.
Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
