#!/bin/bash

path=$(dirname $0)

"$path/server.py" "$@" 2>/dev/null &
"$path/worker.py" "$@" 2>/dev/null &

disown -a
