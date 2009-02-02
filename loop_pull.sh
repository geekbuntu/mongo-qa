#!/bin/bash

#
#  github has it's bad days - so lets just do several tries
#

for i in 1 2 3 4 5 ; do
  git pull
  if [ $? -eq 0 ]; then
    break
  fi
done

