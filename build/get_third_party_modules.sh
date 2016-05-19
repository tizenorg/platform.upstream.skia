#!/bin/bash

function set_environment() {
  local CURRENT_PUBLIC_IP_ADDRESS="$(curl -s icanhazip.com)"
  local WOOMYUN_PUBLIC_IP_ADDRESS="210.94.41.89"
  
  if [ "$CURRENT_PUBLIC_IP_ADDRESS" == "$WOOMYUN_PUBLIC_IP_ADDRESS" ] ; then
    export http_proxy="http://10.112.1.184:8080"
    export https_proxy="https://10.112.1.184:8080"
  fi
}

function download_third_party_modules() {
  git config --global http.sslVerify false
  git submodule update --init
  pushd third_party/externals/fontconf/src;             git reset --hard f16c3118; popd;
  pushd third_party/externals/giflib;                   git reset --hard ab10e256; popd;
  pushd third_party/externals/gyp;                      git reset --hard 08429da7; popd;
  pushd third_party/externals/icu;                      git reset --hard ce41627e; popd;
  pushd third_party/externals/jsoncpp;                  git reset --hard 7165f6ac; popd;
  pushd third_party/externals/libjpeg-turbo;            git reset --hard e4e75037; popd;
  pushd third_party/externals/libpng;                   git reset --hard 070a616b; popd;
  pushd third_party/externals/libwebp;                  git reset --hard 37f04949; popd;
  pushd third_party/externals/nanomsg;                  git reset --hard 0e74bcc8; popd;
  pushd third_party/externals/sfntly;                   git reset --hard 1bdaae8f; popd;
  pushd third_party/externals/yasm/source/patched-yasm; git reset --hard 4671120c; popd;
}

set_environment
download_third_party_modules
