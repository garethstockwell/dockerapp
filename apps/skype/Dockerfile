# skype/Dockerfile

FROM debian:jessie
MAINTAINER Gareth Stockwell <gareth.stockwell.dev@gmail.com>

# Tell debconf to run in non-interactive mode
ENV DEBIAN_FRONTEND noninteractive

# Setup multiarch because Skype is 32bit only
RUN dpkg --add-architecture i386 && \
    apt-get update && apt-get install -y --no-install-recommends \
        curl

ENV SKYPE_VERSION 4.3.0.37-1

RUN curl http://download.skype.com/linux/skype-debian_${SKYPE_VERSION}_i386.deb > /usr/src/skype.deb && \ 
    dpkg --force-depends -i /usr/src/skype.deb && \
    apt-get install -fy \
    && rm -rf /var/lib/apt/lists/*

ENV HOME /home/user
ARG USER_UID
RUN useradd --create-home --home-dir $HOME user --uid $USER_UID \
    && chown -R user:user $HOME \
    && usermod -a -G audio,video user
WORKDIR $HOME
USER user

ENTRYPOINT [ "skype" ]

