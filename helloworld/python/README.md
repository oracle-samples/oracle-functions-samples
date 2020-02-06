# Oracle Functions Python Hello World

Create and deploy your first Python function on Oracle Functions.

Start by logging in to your development environment as an Oracle Functions developer

## Pre-requiste: Create an application

Start by [creating an application](create-application.md)

## Bootstrap a Python function

 Create a Python function by entering:

`fn init --runtime python helloworld-func-python`

A directory called `helloworld-func-python` is created, containing:

- the `func.py` file which contains your actual Python function
- a function definition file called `func.yaml`
- `requirements.txt` which specifies all the dependencies for your Python function.

## Deploy your function

Change directory to the `helloworld-func-python` directory created in the previous step:

`cd helloworld-func-python`

Enter the following single command to build the function and its dependencies as a Docker image called `helloworld-func-python`, push the image to the specified Docker registry, and deploy the function to Oracle Functions:

`fn -v deploy --app helloworld-app`

## Invoke your function

Invoke the `helloworld-func-python` function by entering:

`fn invoke helloworld-app helloworld-func-python`

The `{"message":"Hello World!"}` output is displayed.

You can also pass in a payload to invoke the function:

`echo -n '{"name":"Bob"}' | fn invoke helloworld-app helloworld-func-python`

The `{"message":"Hello Bob!"}` output is displayed.

Congratulations! You've just created, deployed, and invoked your first Python function using Oracle Functions!
