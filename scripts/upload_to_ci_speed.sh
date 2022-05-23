#!/usr/bin/env bash

#upload test xml to ci-speed

set -e

PROJECT_NAME=$1

BUILD_REF=$2

echo "Project: ${PROJECT_NAME} Build: ${BUILD_REF}"

curl --fail-with-body -X 'POST' \
  'https://ci-speed.herokuapp.com/api/test_runs/' \
  -H 'accept: application/json' \
  -H 'Authentication-Token: ${CI_SPEED_AUTH_TOKEN}' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@test_results.xml;type=text/xml' \
  -F 'project_name=${PROJECT_NAME}' \
  -F 'build_ref=${BUILD_REF}'
