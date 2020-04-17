# Invoke Oracle Functions by Id using the OCI Java SDK

This example demonstrates how to invoke a function deployed to Oracle Functions
by its id using the Oracle Cloud Infrastructure Java SDK.

The OCI Java SDK exposes two endpoints specificially for Oracle Functions:

- `FunctionsManagementClient` - which provides APIs for function and application
  lifecycle management
- `FunctionsInvokeClient` - for invoking functions

The SDK also provides a number of utility classes for building function
invocation requests and handling request results.

In this example, we'll invoke an existing function by it's id so we will only 
need the FunctionsInvokeClient. The key method we're going to use is the
suitably named `invokeFunction`, which takes an `InvokeFunctionRequest`.

The set of required steps are:

1. Authenticate with OCI (more on this below)
2. Create a `FunctionsInvokeClient` with the auth credentials
3. Set the `invokeEndpoint` of the client to the invoke endpoint URL of your 
function
4. Create an `InvokeFunctionRequest` with the function id
5. Pass the `InvokeFunctionRequest` to the `FunctionsInvokeClient`to call the
 function
6. Extract the result from an `InvokeFunctionResponse`


## Pre-requisites

1. Clone this repository

   >```
   >git clone https://github.com/<github-user-name>/fn-java-sdk-invokebyid.git
   >```

2. Install/update the Fn CLI

   >```
   >curl -LSs https://raw.githubusercontent.com/fnproject/cli/master/install | sh
   >```

3. Create a function to invoke

   Create a function using [Java Hello World
   Function](https://github.com/abhirockzz/oracle-functions-hello-worlds/blob/master/java-hello-world.md)

## Build the JAR and configure your environment

1. Then build the client JAR:

   >```
   >mvn clean package
   >```

   NOTE: You must update the `pom.xml` properties if you're using a version
   of OCI Java SDK other than "1.8.0".

2. Define OCI authentication properties

   Functions clients need to authenticate with OCI before being able to make
   service calls. There are a few ways to authenticate. This example uses the
   `ConfigFileAuthenticationDetailsProvider`, which reads user properties from
   your OCI config file located in `~/.oci/config`. We will pass the user 
   profile as a command line argument to this program.
    
   Review your ~/.oci/config file to become familiar with its contents and 
   structure. In a terminal type:
    
   >```
   > cat ~/.oci/config
   >```
   
   You should have something like the following in your OCI `config` file:

   ```shell
   [oci-profile]
   region=<your-OCI-region>
   tenancy=<OCID-of-your-tenancy>
   user=<OCID-of-the-OCI-user>
   fingerprint=<public-key-fingerprint>
   key_file=<location-of-the-private-key-on-your-machine>
   pass_phrase=<keyfile-pass-phrase>
   ```

   > NOTE: `pass_phrase` is only required if your private key has a passphrase

## You can now invoke your function!

The Maven build produces a jar in the target folder. The syntax to run the
example is:

>`java -jar target/<jar-name>.jar <oci-profile> <function-invoke-endpoint>
> <function-id> [<optional-payload-string>]`

To find the invoke endpoint for your function, inspect the function you want
 to invoke using the Fn CLI, e.g.,:

>```
>fn inspect fn helloworld-app helloworld-func-java
>```

The result will be a JSON structure similar to the following:

```JSON
{
	"annotations": {
		"fnproject.io/fn/invokeEndpoint": "https://toyh4yqssuq.us-phoenix-1.functions.oci.oraclecloud.com/20181201/functions/ocid1.fnfunc.oc1.iad.aaa...3ua/actions/invoke",
		"oracle.com/oci/compartmentId": "ocid1.compartment.oc1..aaa...jia",
		"oracle.com/oci/imageDigest": "sha256:dfa...eb0"
	},
	"app_id": "ocid1.fnapp.oc1.iad.aaa...pka",
	"created_at": "2019-09-20T08:14:44.973Z",
	"id": "ocid1.fnfunc.oc1.iad.aaa...3ua",
	"idle_timeout": 30,
	"image": "iad.ocir.io/tenant-name/repo-name/java-fn:0.0.5",
	"memory": 128,
	"name": "java-fn",
	"timeout": 30,
	"updated_at": "2019-09-20T08:14:44.973Z"
}
```

The invoke endpoint you need to pass to the example can be extracted from the 
value of the `fnproject.io/fn/invokeEndpoint` property. You just need the
protocol and hostname. For the example above, this would be 
`https://toyh4yqssuq.us-phoenix-1.functions.oci.oraclecloud.com`.  
The `id` property contains the function id.

> NOTE: Payload is optional. If your function doesn't expect any input you
> can omit it.

e.g., without payload:

>```
>java -jar target/fn-java-sdk-invokebyid-1.0-SNAPSHOT.jar workshop https://toyh4yqssuq.us-phoenix-1.functions.oci.oraclecloud.com ocid1.fnfunc.oc1.iad.aaa...3ua
>```

e.g., with payload:

>```
>java -jar target/fn-java-sdk-invokebyid-1.0-SNAPSHOT.jar workshop https://toyh4yqssuq.us-phoenix-1.functions.oci.oraclecloud.com ocid1.fnfunc.oc1.iad.aaa...3ua '{"name":"foobar"}'
>```

## What if my function needs input in binary form?

See the [Invoke by Function name](https://github.com/abhirockzz/fn-java-sdk-invoke) 
example for details on how to attach a binary payload to an
 `InvokeFunctionRequest`.

## Troubleshooting

1. If you provide an invalid function id you'll get an exception similar to
   the following:

   ``` 
   Exception in thread "main" com.oracle.bmc.model.BmcException: (404, NotAuthorizedOrNotFound, false) Authorization failed or requested resource not found (opc-request-id: AEF8EE09761E42D7AA41F524E0/01DNABM56B1BT0E3RZJ0002AX8/01DNABM56B1BT0E3RZJ0002AX9)
   ```

2. If you provide an incorrect `tenancy` or `user` or `fingerprint` in your
   OCI `config` file you'll receive an authentication exception similar to the
   following:

   ``` 
   Exception in thread "main" com.oracle.bmc.model.BmcException: (401, Unknown, false) Unexpected Content-Type: application/json;charset=utf-8 instead of application/json. Response body: {"code":"NotAuthenticated","message":"Not authenticated"} (opc-request-id: 3FD3E66DF81F4BB490A6424530/01D5427GTX1BT1D68ZJ0003Z9E/01D5427GTX1BT1D68ZJ0003Z9F)
   ```
   
