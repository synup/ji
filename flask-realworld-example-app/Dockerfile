######## Make a upstream image to avoid dependency on apline mirrors
# FROM REPO/base:flask-realworld-example-app-latest
FROM python:3.7.3-alpine3.8
LABEL maintainer="rahul@rahulwa.com"
ENV BUILD_PACKAGES bash linux-headers build-base git libffi-dev musl-dev libressl-dev
RUN apk add --no-cache --update $BUILD_PACKAGES \
  postgresql-dev \
  && rm -rf /var/cache/apk/*
#######################################################################
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_CTYPE=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8
ARG app_dir=/opt/app
WORKDIR ${app_dir}
RUN pip install pipenv
COPY flask-realworld-example-app/Pipfile* ${app_dir}/
COPY consul_pyconfig/. /opt/consul_pyconfig/
RUN pipenv install --system --deploy --ignore-pipfile
COPY flask-realworld-example-app/. ${app_dir}/
COPY APP-RELEASE APP-RELEASE
RUN printf "\nBUILD TIMESTAMP: \"$(date)\"\n" >> APP-RELEASE
# for development, just an example
# if consul running on host then it can be used as `docker build -t test -f Dockerfile ../` and then `docker run -p 5000:5000 test` (won't on linux unless https://github.com/docker/for-linux/issues/264)
CMD export FLASK_DEBUG=1 FLASK_APP=app-pyconfig.py CONSUL_HOSTNAME=host.docker.internal \
      && if [ ! -d "migrations" ]; then flask db init; fi \
      && flask db migrate \
      && gunicorn app-pyconfig:app -b 0.0.0.0:5000 -w 3
