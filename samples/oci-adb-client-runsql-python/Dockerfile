FROM oraclelinux:7-slim
WORKDIR /function
RUN groupadd --gid 1000 fn && adduser --uid 1000 --gid fn fn

ARG release=19
ARG update=3

RUN  yum-config-manager --disable ol7_developer_EPEL && \
     yum-config-manager --enable ol7_optional_latest && \
     yum-config-manager --enable ol7_oracle_instantclient && \
     yum -y install python3 oracle-release-el7 && \
     yum -y install oracle-instantclient${release}.${update}-basiclite && \
     rm -rf /var/cache/yum
     
RUN mkdir /tmp/dbwallet
RUN chown -R fn:fn /tmp/dbwallet
ENV TNS_ADMIN=/tmp/dbwallet

ADD . /function/
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache --no-cache-dir -r requirements.txt
RUN rm -fr /function/.pip_cache ~/.cache/pip requirements.txt func.yaml Dockerfile README.md

ENV PYTHONPATH=/python
ENTRYPOINT ["/usr/local/bin/fdk", "/function/func.py", "handler"]
