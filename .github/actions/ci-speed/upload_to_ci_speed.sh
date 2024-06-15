#!/usr/bin/env bash

#upload test xml to ci-speed

set -e

PROJECT_NAME=$1
BUILD_REF=$2
COMMIT=$3
RESULTS=$4

HOST=https://ci-speed.herokuapp.com

echo "Project: ${PROJECT_NAME} Build: ${BUILD_REF}"

if [ -f "$RESULTS" ]; then
  curl --fail -X "POST" \
    "${HOST}/api/test_runs/" \
    -H "accept: application/json" \
    -H "Authentication-Token: ${CI_SPEED_AUTH_TOKEN}" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@${RESULTS};type=text/xml" \
    -F "project_name=${PROJECT_NAME}" \
    -F "build_ref=${BUILD_REF}" \
    -F "commit_sha=${COMMIT}"
else
  echo "No results file found"
  exit 1
fi
