# syntax=docker/dockerfile:1

ARG PYTHON_IMAGE_NAME
ARG PYTHON_IMAGE_VERSION

FROM ${PYTHON_IMAGE_NAME}:${PYTHON_IMAGE_VERSION}
WORKDIR /app

#
# Setup env
#

# Don't write .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Don't buffer stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc make gunicorn
RUN pip install --upgrade pip

COPY . /app/
RUN make build

CMD ["gunicorn", "-k eventlet", "-w1", "--timeout 6000", "server:app"]
