FROM fnproject/python:3.6-dev as build-stage
WORKDIR /function
ADD requirements.txt /function/
RUN pip3 install --no-cache --no-cache-dir --upgrade pip && \
      pip3 install --target /python/  --no-cache --no-cache-dir -r requirements.txt && \
	    rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv && \
      chmod -R o+r /function
ADD . /function/
RUN rm -fr /function/.pip_cache

FROM fnproject/python:3.6
RUN microdnf install oracle-epel-release-el8 &&\
      microdnf install ImageMagick &&\
      microdnf remove oracle-epel-release-el8 &&\
      microdnf clean all
WORKDIR /function
COPY --from=build-stage /function /function
COPY --from=build-stage /python /python
ENV PYTHONPATH=/python:/function
ENTRYPOINT ["/python/bin/fdk", "/function/func.py", "handler"]

