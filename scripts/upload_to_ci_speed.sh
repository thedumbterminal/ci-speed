#!/usr/bin/env bash

#upload test xml to ci-speed

set -e

PROJECT_NAME=$1

BUILD_REF=$2

echo "Project: ${PROJECT_NAME} Build: ${BUILD_REF}"
