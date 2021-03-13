# Function Hello World

This function returns the "Hello World" message or "Hello <name>" when you provide a name in the function call payload.

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


## Code, Deploy and Test a function 

### Python

#### Code

The [Python folder](./python) contains the files to deploy the `hello-python` function in Python:
* the code of the function, [func.py](./python/func.py)
* its dependencies, [requirements.txt](./python/requirements.txt)
* the function metadata, [func.yaml](./python/func.yaml)

#### Deploy

![user input icon](./images/userinput.png)

Change directory to *python* and deploy the `hello-python` function using:

```
fn -v deploy --app <app-name>
```

e.g.
```
fn -v deploy --app myapp
```

#### Test

![user input icon](./images/userinput.png)

The command to invoke a function is 
```
fn invoke <app-name> <func-name>
```


To invoke the Python `hello-python` function, run:
```
fn invoke myapp hello-python
```
The Python version displays `{"message":"Hello World"}`


To invoke the Python function with a payload, run: 
```
echo -n '{"name":"Bob"}' | fn invoke myapp hello-python
```
The `{"message":"Hello Bob"}` output is displayed.


Congratulations! You've just created, deployed, and invoked a Python HelloWorld function using Oracle Functions!


### Java

#### Code

The [Java folder](./java) contains the files to deploy the `hello-java` function in Java:
* the code of the function, [src/main/java/com/example/fn/HelloFunction.java](./java/src/main/java/com/example/fn/HelloFunction.java)
* its dependencies, [pom.xml](./java/pom.xml)
* the function metadata, [func.yaml](./java/func.yaml)


#### Deploy

![user input icon](./images/userinput.png)

Change directory to *java* and deploy the `hello-java` function using:

```
fn -v deploy --app <app-name>
```

e.g.
```
fn -v deploy --app myapp
```

#### Test

To invoke the Java `hello-java` function, run:
```
fn invoke myapp hello-java
```
The Java version displays `Hello, world!`



To invoke the Java function with a payload, run: 
```
echo -n "Bob" | fn invoke myapp hello-java
```
The `Hello, Bob!` output is displayed.


Congratulations! You've just created, deployed, and invoked a Java HelloWorld function using Oracle Functions!



### Node, Golang, and Ruby

In this example we used the provided files. However, you can also generate boilerplate HelloWorld function 
files by running the following command from your terminal:
      
```
fn init --runtime <runtime-language> <func-name>
```

where `<runtime-language>` is one of several runtime languages (currently java, python, node, go and ruby are 
supported). Use `fn init --help` to see a list of boilertplate language runtimes.


## Monitoring Functions

Learn how to configure basic observability for your function using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)
