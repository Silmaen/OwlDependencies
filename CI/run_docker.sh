#!/usr/bin/env bash

set -e

DOCKER_IMAGE=registry.argawaen.net/builder/builder-gcc12-ubuntu2204

if [ ! -d $(pwd)/build/${DOCKER_IMAGE} ]; then
  mkdir -p $(pwd)/build/${DOCKER_IMAGE}
fi
if [ ! -d $(pwd)/build/packages ]; then
    mkdir -p $(pwd)/build/packages
    chmod 777 $(pwd)/build/packages
fi
if [ ! -d $(pwd)/build/cache ]; then
    mkdir -p $(pwd)/build/cache
    chmod 777 $(pwd)/build/cache
fi
docker pull $DOCKER_IMAGE
docker run --rm --user $(id -u):$(id -g) --entrypoint /sources/CI/build.sh -v $(pwd)/build/packages:/.edm  -v $(pwd)/build/cache:/.cache -v $(pwd):/sources -v $(pwd)/build/${DOCKER_IMAGE}:/build ${DOCKER_IMAGE}
