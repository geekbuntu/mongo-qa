#!/bin/bash

#
#  github has it's bad days - so lets just do several tries
#

for i in 1 2 3 4 5 6 7 8 9 ; do
  echo "Git attempt $i"
  sleep 2
  git $@
  if [ $? -eq 0 ]; then
    break
  fi
done

