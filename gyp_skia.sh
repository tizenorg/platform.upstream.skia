#!/bin/bash

source $(dirname $0)/build/common.sh

EXTRA_GYP_ARGS="$@"

ADDITIONAL_GYP_PARAMETERS="-Darm_neon=0
                           -Darm_version=7 
                           -Darm_neon_optional=1
                           -Dclang=0
                           -Dbuilding_for_tizen=1
                           -Dskia_arch_type=arm
                           -Dskia_clang_build=0
                           -Dskia_egl=1
                           -Dskia_skip_gui=1
                           -Dskia_warnings_as_errors=0
                           -Duse_system_libjpeg=1
                           -Duse_x11=0
                           -Dtest=0
                           -Dv8_target_arch=$(getHostArch)
                          "
export OS="tizen"
export skia_os="tizen"

_GYP_ARGS="$EXTRA_GYP_ARGS
           $ADDITIONAL_GYP_PARAMETERS
          "

echo "GYP_ARGUMENTS:"
for arg in $_GYP_ARGS; do
  printf "    * ${arg##-D}\n"
done

./gyp_skia ${_GYP_ARGS}
