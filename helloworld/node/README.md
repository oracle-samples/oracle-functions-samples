# Oracle Functions Nodejs Hello World

Create and deploy your first Nodejs function on Oracle Functions.

Start by logging in to your development environment as an Oracle Functions developer

## Pre-requiste: Create an application

Start by [creating an application](create-application.md)

## Bootstrap a Nodejs function

 Create a Nodejs function by entering:

`fn init --runtime node helloworld-func-node`

A directory called `helloworld-func-node` is created, containing:

- the `func.js` file which contains your actual Node function
- a function definition file called `func.yaml`
- `package.json` which specifies all the Node.js dependencies for your Node function.

## Deploy your function

Change directory to the `helloworld-func-node` directory created in the previous step:

`cd helloworld-func-node`

Enter the following single command to build the function and its dependencies as a Docker image called `helloworld-func-node`, push the image to the specified Docker registry, and deploy the function to Oracle Functions:

`fn -v deploy --app helloworld-app`

## Invoke your function

Invoke the `helloworld-func-node` function by entering:

`fn invoke helloworld-app helloworld-func-node`

The `{"message":"Hello World!"}` output is displayed.

You can also pass in a payload to invoke the function:

`echo -n '{"name":"Bob"}' | fn invoke helloworld-app helloworld-func-node`

The `{"message":"Hello Bob!"}` output is displayed.

Congratulations! You've just created, deployed, and invoked your first Nodejs function using Oracle Functions!

