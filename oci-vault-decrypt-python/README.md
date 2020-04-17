# Function that decrypts a cipher text using Vault keys
This function decrypts a cipher text using a Vault key. As a best practice, we do not recommend to expose your secrets via a return value of a function. This sample just demonstrate to use Vault keys in a function.

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

## Create or Update Policies
Create a new policy that allows the dynamic group to manage compute instances. We will grant `use` access to `keys` in the compartment.

![user input icon](./images/userinput.png)

Your policy should look something like this:
```
Allow dynamic-group <your dynamic group name> to use keys in compartment <your compartment name>
```
e.g.
```
Allow dynamic-group demo-func-dyn-group to use keys in compartment demo-func-compartment
```

For more information on how to create policies, go [here](https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policysyntax.htm).


## Create or select an Application to run your function
You can use an application already created or create a new one as follow:
![user input icon](./images/userinput.png)
```
fn create app <app-name> --annotation oracle.com/oci/subnetIds='["<subnet-ocid>"]'
```
Get the OCID of the subnet in your VCN you wish to use.

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

## Create the Vault key and a cipher text
![user input icon](./images/userinput.png)

On the OCI console, navigate to *Security* > *Key Management*. If you don't already have a Vault created, create one. Create a key by clicking on `Create Key`. Provide a name for the key and click `Create Key`. 

In your vault, note the *Cryptographic Endpoint* and your key OCID.

![Cryptographic Endpoint anf Key OCID](./images/vault.png)

Set the `KEY_OCID` and `CRYPTOGRAPHIC_ENDPOINTT` environement variables with the OCID of your Vault key and the Vault Endpoint. For example:
```
KEY_OCID='ocid1.key.oc1.phx.acdfdfna.abyxxxxxxxsqhycfq'
CRYPTOGRAPHIC_ENDPOINT='https://a5pdddfdfna-crypto.kms.us-phoenix-1.oraclecloud.com'
```

Set the `PLAIN_TEXT` environement variable with the text you will encrypt:
```
PLAIN_TEXT="my text"
```
Run the following command to get the encrypted version of your text:
```
oci kms crypto encrypt --key-id "$KEY_OCID" --endpoint "$CRYPTOGRAPHIC_ENDPOINT" \
    --plaintext "$( echo $PLAIN_TEXT | base64 -b0 )" | jq -r .data.ciphertext
```
The above command is for MacOS. For Linux, replace `base64 -b0` with `base64 -w0`.

The command returns a Cipher text, you will use it to invoke your function.


## Set the function configuration values
The function requires the following configuration values to be set:
- key_ocid
- cryptographic_endpoint

![user input icon](../images/userinput.png)

Use the *fn* CLI to set the config value:
```
fn config function <your app name> <function name> key_ocid <Vault key OCID>
fn config function <your app name> <function name> cryptographic_endpoint <Vault Cryptographic Endpoint>
```
e.g.
```
fn config function gregapp1 oci-vault-decrypt-python  key_ocid  "ocid1.key.oc1.phx.a5pedhchaafna.abyhqljt63augu4nwptqrvaw7gymh7zp7ihvgayo72pehd3sqhfproiaycfq"
fn config function gregapp1 oci-vault-decrypt-python  cryptographic_endpoint 'https://a5pedhchaafna-crypto.kms.us-phoenix-1.oraclecloud.com'
```


## Invoke the function
The function requires the following keys in the payload to be invoked:
- cipher, this is encrypted text you generated in the section [Create the Vault key and a cipher text](#Create the Vault key and a cipher text)

![user input icon](./images/userinput.png)
```
echo '{"cipher": "<your encrypted text>"}' | fn invoke <your app name> oci-vault-decrypt-python
```
e.g.:
```
echo '{"cipher": "Ia+hS8+UYAEV8gr00ItHxsC1jhfslbzAA="}' | fn invoke myapp oci-vault-decrypt-python
```

Upon success, the function should return the decrypted text:
{"decryptedtext": "my text"}