#!/bin/bash

PATH_DOCKERAPP=$(builtin cd "$(dirname ${BASH_SOURCE[0]:-$0})/.." && pwd)

export PATH=$PATH:$PATH_DOCKERAPP/bin

function command_not_found_handle
{
    # Check if there is a container image with that name
    if ! docker inspect --format '{{ .Author }}' "$1" >&/dev/null; then
        echo "$0: $1: command not found"
        return
    fi

    # Check that it's really the name of the image, not a prefix
    if docker inspect --format '{{ .Id }}' "$1" | grep -q "^$1" ;then
        echo "$0: $1: command not found"
        return
    fi

    # Check if we are on a tty to decide whether to allocate one
    DOCKERAPP_TTY=
    tty -s && DOCKERAPP_TTY=--tty

    dockerapp run $DOCKERAPP_TTY "$@"
}

