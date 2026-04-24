#!/usr/bin/env bash

remote_url=$1
remote_login=$2
remote_passwd=$3

set -e
poetry install --no-interaction --with build
depmanager info version
depmanager remote add -vv -n pack -d -u ${remote_url} -l ${remote_login} -p ${remote_passwd}
depmanager remote ls -vv
