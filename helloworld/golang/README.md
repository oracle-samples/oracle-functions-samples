# Oracle Functions Golang Hello World

Create and deploy your first Golang function on Oracle Functions.

Start by logging in to your development environment as an Oracle Functions developer

## Pre-requiste: Create an application

Start by [creating an application](create-application.md)

## Bootstrap a Golang function

 Create a Golang function by entering:

`fn init --runtime go helloworld-func-go`

A directory called `helloworld-func-go` is created, containing:

- the `func.go` file which contains your actual Go function
- a function definition file called `func.yaml`
- `Gopkg.toml` is the dependency management tool file which specifies all the dependencies for your function

## Deploy your function

Change directory to the `helloworld-func-go` directory created in the previous step:

`cd helloworld-func-go`

Enter the following single command to build the function and its dependencies as a Docker image called `helloworld-func-go`, push the image to the specified Docker registry, and deploy the function to Oracle Functions:

`fn -v deploy --app helloworld-app`

## Invoke your function

Invoke the `helloworld-func-go` function by entering:

`fn invoke helloworld-app helloworld-func-go`

The `{"message":"Hello World!"}` output is displayed.

You can also pass in a payload to invoke the function:

`echo -n '{"name":"Bob"}' | fn invoke helloworld-app helloworld-func-go`

The `{"message":"Hello Bob!"}` output is displayed.

Congratulations! You've just created, deployed, and invoked your first Golang function using Oracle Functions!

