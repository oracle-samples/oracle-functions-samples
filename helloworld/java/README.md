# Oracle Functions Java Hello World

Create and deploy your first Java function on Oracle Functions.

Start by logging in to your development environment as an Oracle Functions developer

## Pre-requiste: Create an application

Start by [creating an application](create-application.md)

## Bootstrap a Java function

 Create a Java function by entering:

`fn init --runtime java helloworld-func-java`

A directory called `helloworld-func-java` is created, containing:

A directory called helloworld-func is created, containing:

- a function definition file called `func.yaml`
- a `/src` directory containing source files and directories for the function
- a Maven configuration file called `pom.xml` that specifies the dependencies required to compile the function

## Deploy your function

Change directory to the `helloworld-func-java` directory created in the previous step:

`cd helloworld-func-java`

Enter the following single command to build the function and its dependencies as a Docker image called `helloworld-func-java`, push the image to the specified Docker registry, and deploy the function to Oracle Functions:

`fn -v deploy --app helloworld-app`

## Invoke your function

Invoke the `helloworld-func-java` function by entering:

`fn invoke helloworld-app helloworld-func-java`

The `Hello, world!` output is displayed.

You can also pass in a payload to invoke the function:

`echo -n 'Bob' | fn invoke helloworld-app helloworld-func-java`

The `Hello, Bob!` output is displayed.

Congratulations! You've just created, deployed, and invoked your first Java function using Oracle Functions!

