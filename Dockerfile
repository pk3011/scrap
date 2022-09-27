FROM ubuntu:22.04

WORKDIR /usr/src/app
SHELL ["/bin/bash", "-c"]
RUN chmod 777 /usr/src/app

RUN apt-get -y update && DEBIAN_FRONTEND="noninteractive" \
    apt-get install -y apt-utils && DEBIAN_FRONTEND="noninteractive" \
    apt-get install -y python3 python3-pip wget \
	libglib2.0 libnss3 libgconf-2-4 libfontconfig1 \
    tzdata pv jq locales git \
    && locale-gen en_US.UTF-8 && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update && apt-get -y install google-chrome-stable

ENV LANG="en_US.UTF-8" LANGUAGE="en_US:en"

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash","start.sh"]