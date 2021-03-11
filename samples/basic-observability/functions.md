# Basic Guidance for Monitoring your Functions

This guide shows how you can use a simple email alert to monitor the status of your functions.

For more details, refer to the [technical documentation](https://docs.oracle.com/en-us/iaas/Content/Functions/Reference/functionsmetrics.htm).


## Create a topic and a subscription for the Notification Service

1. From the [OCI Console](https://cloud.oracle.com) navigation menu, select **Application Integration**, and then select **Notifications**

2. Click **Create Topic** and create a topic with **my_function_status** name

3. Choose your topic, click **Create Subscription** and create a subscription with your email:
    * **Protocol**: Select Email 
    * **Email**: Enter your email address

4. The subscription will be created in "Pending" status. You will receive a confirmation email 
and will need to click on the link in the email to confirm your email address.


## Check Metrics and create an alarm definition from Metrics

1. From the navigation menu, select **Developer Services**, and then select **Functions**

2. Choose the application and the function that you want to monitor

3. From the Metrics page, go to the "Functions Errors" chart, click on **Options** and **Create an Alarm on this Query**

4. Add a **name** and under **Notifications** select **Destination service** as notification service, select the compartment **your_compartment**, and select **Topic** as my_function_status



## Create an alarm definition from scratch

1. From the navigation menu, select **Monitoring**, and then select **Alarm Definitions**

2. Click **Create Alarm** and use the following example:
    * **Alarm Name**: my_function_status
    * **Alarm severity**: Critical
    * **Alarm body**: OCI Alarm: my function 

3. On **Metric description** select the compartment **your_compartment**, select **Metric namespace** as oci_faas, **Metric name** as FunctionResponseCount, **Interval** as 1m, and **Statistic** as Mean

4. On **Trigger rule** select Value greater than 1

6. On **Notification** select **Destination service** as notification service, select the compartment **your_compartment**, and select **Topic** as my_function_status
