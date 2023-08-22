ARG STATIC_ROOT=/data/static
# The ID of the user running in the container
ARG DOCKER_USER=10000

FROM python:3.9.10-slim as base

# Install extra software
RUN apt-get update && \
    apt-get install -y \
    git gettext python3-dev default-libmysqlclient-dev build-essential pkg-config && \
    rm -rf /var/lib/apt/lists/*

# ---- back-end builder image ----
FROM base as back-builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /builder

# Copy required python dependencies
COPY ./src/backend/requirements/base.txt /builder/requirements.txt

# install python dependencies
RUN pip install --upgrade pip

RUN mkdir /install
RUN pip install --prefix=/install --no-cache-dir -r /builder/requirements.txt


# ---- Core application image ----
FROM base as core

ENV ALLOWED_HOSTS localhost:8000
ENV CSRF_TRUSTED_ORIGINS http://localhost:8000

ENV MYSQL_DATABASE swissmooc-extras
ENV MYSQL_USER swissmooc-extras
ENV MYSQL_PASSWORD password

# Copy installed python dependencies
COPY --from=back-builder /install /usr/local

# Copy runtime-required files
COPY ./src/backend /app
COPY ./docker/files/usr/local/bin/entrypoint /usr/local/bin/entrypoint

WORKDIR /app

# Make sure .mo files are up-to-date
RUN mkdir -p locale && python manage.py compilemessages

# Gunicorn
RUN mkdir -p /usr/local/etc/gunicorn
COPY ./docker/files/usr/local/etc/gunicorn/app.py /usr/local/etc/gunicorn/app.py

# Give the "root" group the same permissions as the "root" user on /etc/passwd
# to allow a user belonging to the root group to add new users; typically the
# docker user (see entrypoint).
RUN chmod g=u /etc/passwd

# We wrap commands run in this container by the following entrypoint that
# creates a user on-the-fly with the container user ID (see USER) and root group
# ID.
ENTRYPOINT [ "/usr/local/bin/entrypoint" ]

# ---- Static files/links collector ----
FROM core as collector

ARG STATIC_ROOT

# Install rdfind
RUN apt-get update && \
    apt-get install -y \
    rdfind && \
    rm -rf /var/lib/apt/lists/*

# Collect static files
RUN python manage.py collectstatic --noinput

# Replace duplicated file by a symlink to decrease the overall size of the final image
RUN rdfind -makesymlinks true ${STATIC_ROOT}

# ---- Development image ----
FROM core as development

# Copy required python dependencies
COPY ./src/backend/requirements/development.txt /tmp/requirements.txt

# Install development dependencies
RUN pip install -r /tmp/requirements.txt

# Un-privileged user running the application
ARG DOCKER_USER
USER ${DOCKER_USER}

# Run django development server
CMD python manage.py runserver 0.0.0.0:8000

# ---- Production image ----
FROM core as production

ARG DOCKER_USER
ARG STATIC_ROOT

# Un-privileged user running the application
USER ${DOCKER_USER}

# The default command runs gunicorn WSGI server in the sandbox
CMD gunicorn -c /usr/local/etc/gunicorn/app.py core.wsgi:application

# ---- Nginx ----
FROM nginx:1.21.6 as nginx

ARG STATIC_ROOT

RUN mkdir -p ${STATIC_ROOT}

COPY --from=collector ${STATIC_ROOT} ${STATIC_ROOT}

RUN rm /etc/nginx/conf.d/default.conf

COPY ./docker/files/etc/nginx/conf.d/swissmooc-extras-app.conf /etc/nginx/conf.d/swissmooc-extras-app.conf
