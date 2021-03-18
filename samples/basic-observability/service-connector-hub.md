# Basic Guidance for Monitoring your Service Connectors

This guide shows how you can use a simple email alert to monitor the status of your Service Connectors.

For more details, refer to the [technical documentation](https://docs.oracle.com/en-us/iaas/Content/service-connector-hub/metrics.htm).

## Create a topic and a subscription for the Notification Service

1. From the [OCI Console](https://cloud.oracle.com) navigation menu, select **Application Integration**, and then select **Notifications**

2. Click **Create Topic** and create a topic with **my_sch_status** name

3. Choose your topic, click **Create Subscription** and use the following example:
    * **Protocol**: Select Email 
    * **Email**: Enter your email address

4. The subscription will be created in "Pending" status. You will receive a confirmation email 
and will need to click on the link in the email to confirm your email address.


## Check Metrics and create an alarm definition from Metrics

1. From the navigation menu, select **Logging**, and then select **Service Connectors**

2. Choose the connector that you want to monitor and click on **Metrics** link under **Resources** in the left navigation pane

3. From the metrics chart that you want to add the alarm e.g., "Service Connector Hub Errors", click on **Options** and **Create an Alarm on this Query**

4. Add a **name** and on **Notification** select **Destination service** as notification service, select the compartment **your_compartment**, and select **Topic** as my_sch_status


## Create an alarm definition from scratch

1. From the navigation menu, select **Monitoring**, and then select **Alarm definitions**

2. Click **Create Alarm** and use the following example:
    * **Alarm Name**: my_sch_status
    * **Alarm severity**: Critical
    * **Alarm body**: OCI Alarm: my sch 

3. On **Metric description** select the compartment **your_compartment**, select **Metric namespace** as oci_service_connector_hub, **Metric name** as ServiceConnectorHubErros, **Interval** as 1m, and **Statistic** as Mean

4. On **Trigger rule** select Value greater or equal than 1

6. On **Notification** select **Destination service** as notification service, select the compartment **your_compartment**, and select **Topic** as my_sch_status
