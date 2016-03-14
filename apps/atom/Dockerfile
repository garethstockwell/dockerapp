FROM debian:jessie
MAINTAINER Jessica Frazelle <jess@docker.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        gconf2 \
        gconf-service \
        gvfs-bin \
        libasound2 \
        libgconf-2-4 \
        libgnome-keyring-dev \
        libgtk2.0-0 \
        libnotify4 \
        libnss3 \
        libxtst6 \
        xdg-utils \
    && \
    rm -rf /var/lib/apt/lists/*

ENV ATOM_VERSION 1.5.1

RUN buildDeps=' \
        ca-certificates \
        curl \
    ' \
    && set -x \
    && apt-get update && apt-get install -y $buildDeps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://github.com/atom/atom/releases/download/v${ATOM_VERSION}/atom-amd64.deb -o /tmp/atom-amd64.deb \
    && dpkg -i /tmp/atom-amd64.deb \
    && rm -rf /tmp/*.deb \
    && apt-get purge -y --auto-remove $buildDeps

ENV HOME /home/user

ARG USER_UID
RUN useradd --create-home --home-dir $HOME user --uid $USER_UID \
    && chown -R user:user $HOME

WORKDIR $HOME
USER user

ENTRYPOINT [ "atom", "--foreground" ]

