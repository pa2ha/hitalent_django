FROM ubuntu:22.04

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    dos2unix \
    && ln -s /bin/python3 /usr/bin/python \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt


COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

RUN dos2unix /usr/src/app/entrypoint.sh && \
    chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]