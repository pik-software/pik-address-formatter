#!/bin/bash
set -e

die() { echo "$*" 1>&2 ; exit 1; }

VERSION=$(python setup.py --version)

LAST_VERSION=$(git describe --tags --abbrev=0 --match v*)
LAST_VERSION=${LAST_VERSION:1}

if [[ ${LAST_VERSION} == ${VERSION} ]]; then
	die "You should update release VERSION"
fi

echo "CURRENT VERSION: $LAST_VERSION"
echo "NEW VERSION: $VERSION"

python setup.py sdist bdist_wheel

echo -e "[pypi]" >> ~/.pypirc
echo -e "username = $PYPI_LOGIN" >> ~/.pypirc
echo -e "password = $PYPI_PASSWORD" >> ~/.pypirc

python -m twine upload dist/*
