# syntax=docker/dockerfile:1

ARG PYTHON_IMAGE_NAME
ARG PYTHON_IMAGE_VERSION

FROM ${PYTHON_IMAGE_NAME}:${PYTHON_IMAGE_VERSION}

#
# Setup env
#

# Don't write .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Don't buffer stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install requirements
RUN apt-get update && \
    apt-get install -y --no-install-recommends make

# Add a user
RUN useradd -d /app -ms /bin/bash pyldes
USER pyldes
WORKDIR /app

# Setup the applicaton
COPY --chown=pyldes:pyldes . /app/
RUN make build

CMD ["make", "run"]