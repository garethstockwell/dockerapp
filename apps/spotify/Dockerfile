# spotify/Dockerfile

FROM ubuntu:14.04
MAINTAINER Jessie Frazelle <jess@linux.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
        alsa-utils \
        libpangoxft-1.0-0 \
        libxss1 \
        software-properties-common \
        xdg-utils \
    && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 94558F59 && \
    echo "deb http://repository.spotify.com stable non-free" >> \
        /etc/apt/sources.list.d/spotify.list && \
    apt-get update && \
    apt-get install --force-yes -y \
        spotify-client \
    && \
    rm -rf /var/lib/apt/lists/*

ENV HOME /home/spotify

ARG DOCKERAPP_UID
RUN useradd --create-home --home-dir $HOME spotify --uid $DOCKERAPP_UID \
    && gpasswd -a spotify audio \
    && chown -R spotify:spotify $HOME

WORKDIR $HOME
USER spotify

# Make search bar text better
RUN echo "QLineEdit { color: #000 }" > /home/spotify/spotify-override.css

ENTRYPOINT [ "spotify" ]
CMD [ "-stylesheet=/home/spotify/spotify-override.css" ]

