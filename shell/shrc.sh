#!/bin/bash

if [ -n "$(declare -f command_not_found_handle)" ]; then
    if [ -z $PATH_DOCKERAPP ]; then
        eval "$(echo "_command_not_found_handle()"; declare -f command_not_found_handle | tail -n +2)"
    fi
fi

PATH_DOCKERAPP=$(builtin cd "$(dirname ${BASH_SOURCE[0]:-$0})/.." && pwd)

export PATH=$PATH:$PATH_DOCKERAPP/bin

function command_not_found_handle
{
    if ! docker inspect --format '{{ .Name }}' "$1" >&/dev/null; then
        _command_not_found_handle $1
        return
    fi

    # Check that it's really the name of the image, not a prefix
    if docker inspect --format '{{ .Id }}' "$1" | grep -q "^$1" ;then
        _command_not_found_handle $1
        return
    fi

    # Check if we are on a tty to decide whether to allocate one
    DOCKERAPP_TTY=
    tty -s && DOCKERAPP_TTY=--tty

    dockerapp run $DOCKERAPP_TTY "$@"
}

