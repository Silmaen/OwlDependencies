#!/usr/bin/env bash

set -e

pull=$1
push=$2

if [ "$pull" = "yes" ]; then
  echo "depmanager remote sync --pull-only"
  depmanager remote sync --pull-only
fi

echo "cmake -S /sources -B /build"
cmake -S /sources -B /build
echo "cmake --build build --target all"
cmake --build build --target all

if [ "$push" = "yes" ]; then
  echo "depmanager remote sync --push_only"
  depmanager remote sync --push_only
fi
