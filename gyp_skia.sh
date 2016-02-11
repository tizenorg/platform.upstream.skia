#!/bin/bash

source $(dirname $0)/build/common.sh

EXTRA_GYP_ARGS="$@"

ADDITIONAL_GYP_PARAMETERS="-Dclang=0
                           -Dv8_target_arch=$(getHostArch)
                           -Dbuilding_for_tizen=1
                          "

_GYP_ARGS="$EXTRA_GYP_ARGS
           $ADDITIONAL_GYP_PARAMETERS
          "

echo "GYP_ARGUMENTS:"
for arg in $_GYP_ARGS; do
  printf "    * ${arg##-D}\n"
done

./gyp_skia ${_GYP_ARGS}
