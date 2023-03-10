#!/bin/sh
set -e

# ls -la ${CKAN_VENV}/bin/activate
. ${CKAN_VENV}/bin/activate

export _ROOT=${CKAN_VENV}/src/ckanext-${PLUGIN}
# export _ROOT=${CKAN_VENV}/src/${PLUGIN}

cd ${_ROOT}

python setup.py develop

${CKAN_VENV}/bin/pytest --ckan-ini=./test.ini ckanext/${PLUGIN}/tests