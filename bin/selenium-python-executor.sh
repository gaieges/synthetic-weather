#!/bin/bash

seleniumtest=$1

if ! [ -f $seleniumtest ]; then
  >&2 echo "file not found: $seleniumtest" && exit 1
fi

export DISPLAY=:1
if ! pgrep Xvfb >/dev/null ; then
  /usr/bin/Xvfb $DISPLAY &> /var/log/Xvfb.log &
fi

python $seleniumtest #2> /dev/null
