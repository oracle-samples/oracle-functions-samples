## Tracing Functions with APM and Zipkin
 
This is an example to show how you can use APM Tracing and Zipkin to trace your function code.

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


## Create or Update IAM Policies

Create a new policy that allows the user group to manage apm-domains in the compartment. 

Create a new policy that allows service FaaS to use apm-domains in the compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow group <user-group-name> to manage apm-domains in compartment <compartment-name>
Allow service FaaS to use apm-domains in compartment <compartment-name>
```
e.g.
```
Allow group functions-developers to manage apm-domains in compartment demo-func-compartment
Allow service FaaS to use apm-domains in compartment demo-func-compartment
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Create an APM Domain

First, you need to create an APM Domain. 

1. From the [OCI Console](https://cloud.oracle.com) navigation menu, select **Application Performance Monitoring**, and then select **Administration**.

2. Select the compartment **demo-func-compartment** that you created.

3. Click **Create APM Domain**. Enter a Name **demo-apm-domain**, and a suitable Description. Select a Compartment, and optionally, select "Create an Always Free Domain".


## Enable tracing on the Functions Application

Next, enable tracing for your Functions Application and select an APM Domain to send traces to.

1. From the [OCI Console](https://cloud.oracle.com) navigation menu, select **Developer Services**, and then select **Functions**.

2. Select the compartment **demo-func-compartment** that you created.

3. Click on the application name to go to the Application Details screen.

4. Click on **Traces** under the **Resources** section.

5. Click on the **Enable Trace** toggle switch. Select the compartment **demo-func-compartment**, and the APM Domain **demo-apm-domain** that you created.


## Review and customize the function

Refer to the readme for each function:

* [Python](./python/README.md)


## Deploy the function

Refer to the readme for each function:

* [Python](./python/README.md)


### Test

Refer to the readme for each function:

* [Python](./python/README.md)


## Monitoring Functions

Learn how to configure basic observability for your function using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)
