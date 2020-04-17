# Execute a SQL statement against Autonomous Database using the Oracle client
This function connects to Oracle Autonomous Database (either Transaction Processing or Data Warehouse) using the Oracle Client and execute a SQL statement. 

As you make your way through this tutorial, look out for this icon ![user input icon](./images/userinput.png).
Whenever you see it, it's time for you to perform an action.


## Pre-requisites
1. Start by making sure all of your policies are correct from this [guide](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionscreatingpolicies.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Tenancy%20for%20Function%20Development%7C_____4)

2. Have [Fn CLI setup with Oracle Functions](https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionsconfiguringclient.htm?tocpath=Services%7CFunctions%7CPreparing%20for%20Oracle%20Functions%7CConfiguring%20Your%20Client%20Environment%20for%20Function%20Development%7C_____0)


## Create or Update your Dynamic Group
In order to use other OCI Services, your function
must be part of a dynamic group. For information on how to create a dynamic group,
go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Tasks/managingdynamicgroups.htm#To).

![user input icon](./images/userinput.png)

When specifying the *Matching Rules*, consider the following examples:
* Matching all functions in a compartment:
```
ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaaaa23______smwa'}
```
* Matching a specific function by its OCID:
```
resource.id = 'ocid1.fnfunc.oc1.iad.aaaaaaaaacq______dnya'
```
* Matching functions with a defined tag (free-form tags are not supported):
```
ALL {resource.type = 'fnfunc', tag.department.operations.value = '45'}
```


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


## Create an Autonomous Database
Use an existing Autonomous Database (either Transaction Processing or Datawarehouse) or create a new one as follows.

![user input icon](./images/userinput.png)

On the OCI console, navigate to *Autonomous Transaction Processing* or *Autonomous Data Warehouse* and click *Create Autonomous Database*. In the Create Autonomous Database dialog, enter the following:
- Display Name
- Compartment
- Database Name
- Infrastructure Type: Shared
- Admin password
- License type

![ADB create](./images/ADB-create.png)
For more information, go to https://docs.cloud.oracle.com/iaas/Content/Database/Tasks/adbcreating.htm


## Database Wallet and IAM Policies
The Database wallet is not part of the Docker image because it is not secure. The function downloads the wallet while it is executed.
The wallet can be retrieved from Object Storage or directly from Autonomous Database.

![user input icon](./images/userinput.png)

If you choose to retrieve the wallet from Object Storage, first download the wallet from Autonomous Database. Navigate to *Autonomous Transaction Processing* or *Autonomous Data Warehouse*, click on your database abd click on *DB Connection*. On the Pop-up window, click *Download Wallet*.

![Download Wallet](./images/Download_wallet.png)

Create a bucket in Object Storage and upload the wallet there. Note the name of the bucket and the wallet object name.
Create an IAM policy that allows the dynamic group to read objects in the bucket. We will grant `read` access to `objects` in your bucket in the compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <your dynamic group name> to read objects in compartment <your compartment name> where target.bucket.name='<bucket-name>'
```
e.g.
```
Allow dynamic-group dg-greg to read objects in compartment greg-verstraeten where target.bucket.name='db-wallets'
```

If you choose to retrieve the wallet from Autonomous Database directly during the execution of the function, note the OCID of the Autonomous Database and create an IAM policy that allows the dynamic group to use the autonomous Database with the specific permission 'AUTONOMOUS_DATABASE_CONTENT_READ'.
```
Allow dynamic-group <your dynamic group name> to use autonomous-databases in compartment <your compartment name> where request.permission='AUTONOMOUS_DATABASE_CONTENT_READ'
```
e.g.
```
Allow dynamic-group mydg to use autonomous-databases in compartment mycompartment where request.permission='AUTONOMOUS_DATABASE_CONTENT_READ'
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Set the function configuration values
The function requires several config value to be set.

![user input icon](../images/userinput.png)

Use the *fn* CLI to set the config value:
```
fn config function <your app name> <function name> DBSVC <DB service name>
fn config function <your app name> <function name> DBUSR <DB username>
fn config function <your app name> <function name> DBPWD_CYPHER <DB encrypted password>
```
Depending on where the DB wallet should be downloaded, specify either the bucket and object name, or the Autonomouns Database OCID:
```
fn config function <your app name> <function name> DBWALLET_BUCKET <DB service name>
fn config function <your app name> <function name> DBWALLET_OBJECT <DB username>
```
or:
```
fn config function <your app name> <function name> ADB_OCID <Autonomous DB OCID>
```
e.g. with a DB wallet in a bucket:
```
fn config function myapp oci-adb-client-runsql-python DBSVC "gregadw_high"
fn config function myapp oci-adb-client-runsql-python DBUSR "admin"
fn config function myapp oci-adb-client-runsql-python DBPWD_CYPHER "dfgjksadhfg4526897dfgkj"
fn config function myapp oci-adb-client-runsql-python DBWALLET_BUCKET "db-wallets"
fn config function myapp oci-adb-client-runsql-python DBWALLET_OBJECT "Wallet_gregADW.zip"
```


## Invoke the function
![user input icon](./images/userinput.png)
```

echo '{"sql_statement":"<sql statement>"}' | fn invoke <your app name> oci-adb-client-runsql-python
```
e.g.:
```
echo '{"sql_statement":"select sysdate from dual"}' | fn invoke myapp oci-adb-client-runsql-python
```

Upon success, the function returns a JSON object similar to this:
```json
{"sql_statement": "select sysdate from dual", "result": "[(datetime.datetime(2020, 2, 27, 20, 19, 42),)]"}
```
