## Tracing Python Functions with APM Tracing and Zipkin

_**Contributed by: Isaac Lipszyc**_

This sample shows how you can trace your Python function code with APM Tracing and Zipkin.

As you make your way through this tutorial, look out for this icon ![user input icon](../images/userinput.png).
Whenever you see it, it's time for you to perform an action.


## Prerequisites

Before you proceed further, ensure you have followed all the steps outlined 
in the parent README file located in [trace-functions-with-apm](../README.md)


## Review and customize the function

Review the following files in the current folder:
* the code of the function, [func.py](./func.py)
* its dependencies, [requirements.txt](./requirements.txt)
* the function metadata, [func.yaml](./func.yaml)


## Deploy the function

In Cloud Shell, run the `fn deploy` command to build *this* function and its dependencies as a Docker image, 
push the image to the specified Docker registry, and deploy *this* function to Oracle Functions 
in the application created earlier:

![user input icon](../images/userinput.png)
```
fn -v deploy --app <app-name>
```
e.g.
```
fn -v deploy --app myapp
```

## Enable tracing for the function

We have already enabled tracing for the Functions application. Now, enable tracing for your function.

1. From the [OCI Console](https://cloud.oracle.com) navigation menu, select **Developer Services**, and then select **Functions**.

2. Select the compartment **demo-func-compartment** that you created.

3. Click on the application name to go to the Application Details screen.

4. Click on **Functions** under the **Resources** section.

5. Click on the **Enable Trace** toggle switch for the function you deployed.


## Test the function

In Cloud Shell, run the following `fn invoke` command to unit test this function:

![user input icon](../images/userinput.png)
```
fn invoke <app-name> <function-name>
```
e.g., 
```
fn invoke myapp apm-fn-int-python
```

You should see your function traces in the APM Trace Explorer.


## View your function traces in the APM Trace Explorer

1. From the [OCI Console](https://cloud.oracle.com) navigation menu, select **Application Performance Monitoring**, and then select **Trace Explorer**.

2. Select the compartment **demo-func-compartment** and the **demo-apm-domain** that you created.

3. Select a time window e.g., "Last 15 minutes".

4. You should see your function traces listed on the page. Click on a trace for your function and it will open the "Trace Details" page and show all your spans and the time taken by each span.

5. Click on one of the spans to get the span details, including errors, if any.

