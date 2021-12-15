# Creating a Function from a Docker Image

This sample walks you through how to use a custom Docker image to define a
function.  Although functions are packaged as Docker images, when
developing functions using the Fn CLI developers are not directly exposed
to the underlying Docker platform.  Docker isn't hidden (you can see
Docker build output and image names and tags), but you aren't
required to be very Docker-savvy to develop functions with Fn.

However, sometimes you need to handle advanced use cases and must take
complete control of the creation of the function container image. Fortunately
the design and implementation of Oracle Functions enables you to do exactly that.
Let's build a simple custom function container image to become familiar with the key
elements of the process.

One of the most common reasons for writing a custom Dockerfile for a function
is to install a Linux package that your function needs.  In our example we're
going to use the the ever-popular [ImageMagick](https://www.imagemagick.org) to
do some image processing in our function and while there are several Python libraries for
ImageMagick, they are just wrappers on the underlying native library.  So we'll
have to install the native library in addition to adding the Python library (Wand) to our
*requirements.txt* dependencies.

As you make your way through this tutorial, look out for this icon.
![](images/userinput.png) Whenever you see it, it's time for you to
perform an action.


## Prerequisites
Before you deploy this sample function, make sure you have run steps A, B and C of the [Oracle Functions Quick Start Guide for Cloud Shell](https://www.oracle.com/webfolder/technetwork/tutorials/infographics/oci_faas_gettingstarted_quickview/functions_quickview_top/functions_quickview/index.html)
* A - Set up your tenancy
* B - Create application
* C - Set up your Cloud Shell dev environment


## Review and customize the function
Review the following files in the current folder:
* the code of the function, [func.py](./func.py)
* the function dependencies, [requirements.txt](./requirements.txt)
* the function metadata, [func.yaml](./func.yaml)
* the function Dockerfile, [Dockerfile](./Dockerfile)

The function takes a binary image as its argument, writes it to a tmp file, and
then uses ImageMagick to obtain the width and height of the image.
There are lots of interesting elements to this function but the key one for us
is the use of the "wand" Python library for ImageMagick image processing.  
To use it we need to include it along with our other dependencies in the
*requirements.txt* file.
With all Python functions, we include the Fn Python FDK as a dependency, in this samples we add
 "wand" for imagemagick image processing.  
This function metadata file *func.yaml* is pretty standard for a Python function except that instead of
declaring the **runtime** as "Python" we specify "**docker**".  
One more small point worthy of note is that if you don't declare the *runtime*
property then it will default to *docker* and the CLI will look for a
Dockerfile.

The Dockerfile that "fn build" would automatically generate to build a
Python 3.6 function container image looks like this:

```Dockerfile
FROM fnproject/python:3.6-dev as build-stage
WORKDIR /function
ADD requirements.txt /function/

RUN pip3 install --target /python/  --no-cache --no-cache-dir -r requirements.txt &&\
  rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv &&\
  chmod -R o+r /python
ADD . /function/
RUN rm -fr /function/.pip_cache
FROM fnproject/python:3.6
WORKDIR /function
COPY --from=build-stage /python /python
COPY --from=build-stage /function /function
RUN chmod -R o+r /function
ENV PYTHONPATH=/function:/python
ENTRYPOINT ["/python/bin/fdk", "/function/func.py", "handler"]
```

It's a two stage build with the first stage containing python with build tools
and the second stage with only the python runtime and minimum required dependencies.
This approach is designed to ensure that deployable function container
images are as small as possible, which is beneficial for a number of reasons
including the time it takes to transfer the image from a Docker respository to
the compute node where the function is to be run.

The *fnproject/python:3.6* container image needs ImageMagick from the EPEL repo, so we'll need to install
the
[ImageMagick package](https://yum.oracle.com/repo/OracleLinux/OL8/developer/EPEL/x86_64/index.html)
using the *microdnf* package management utility.
```Dockerfile
RUN microdnf install oracle-epel-release-el8 &&\
      microdnf install ImageMagick &&\
      microdnf remove oracle-epel-release-el8 &&\
      microdnf clean all
```
We want to install ImageMagick into the runtime image, not the build image, so we need to 
add the above lines in the second stage as shown in the merged [Dockerfile](./Dockerfile).


## Deploy the function
In Cloud Shell, run the *fn deploy* command to build the function and its dependencies as a Docker image, 
push the image to OCIR, and deploy the function to Oracle Functions in your application.

![user input icon](./images/userinput.png)
```
fn -v deploy --app <app-name>
```


## Invoke the function
With the function deployed let's invoke it to make sure it's working as
expected. You'll need a jpeg or png file so either find one on your machine
or download one.  The *3x3.jpg* image in this repo has a height and width of 3 pixels.

![](images/userinput.png)
```
 cat 3x3.jpg | fn invoke <app-name> imagedims-python
```

You should see the following output:

```json
{"width": 3, "height": 3}
```


## Monitoring Functions

Learn how to configure basic observability for your function using metrics, alarms and email alerts:
* [Basic Guidance for Monitoring your Functions](../basic-observability/functions.md)


## Conclusion
One of the most powerful features of Fn and Oracle Functions is the ability to
use custom-defined Docker container images as functions. This feature makes it
possible to customize your function's runtime environment including letting you
install any Linux libraries or utilities that your function might need. And
thanks to the Fn CLI's support for Dockerfiles it's the same user experience as
when developing any function.

