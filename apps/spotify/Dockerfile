# spotify/Dockerfile

FROM ubuntu:14.04
MAINTAINER Gareth Stockwell <gareth.stockwell.dev@gmail.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
        alsa-utils \
        libpangoxft-1.0-0 \
        libxss1 \
        pulseaudio \
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

ENV HOME /home/user

ARG USER_UID
RUN useradd --create-home --home-dir $HOME user --uid $USER_UID \
    && gpasswd -a user audio \
    && chown -R user:user $HOME

WORKDIR $HOME
USER user

# Make search bar text better
RUN echo "QLineEdit { color: #000 }" > /home/user/spotify-override.css

ENTRYPOINT [ "spotify" ]
CMD [ "-stylesheet=/home/user/spotify-override.css --ui.hardware_acceleration=false" ]

