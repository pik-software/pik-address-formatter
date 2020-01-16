#!/bin/bash
set -e
set -x
git checkout master
git pull

die() { echo "$*" 1>&2 ; exit 1; }

VERSION=$(python setup.py --version)
NAME=$(python setup.py --name)

LAST_VERSION=$(git describe --tags --abbrev=0 --match v*)
LAST_VERSION=${LAST_VERSION:1}

if [[ ${LAST_VERSION} == ${VERSION} ]]; then
	die "You should update release VERSION"
fi

echo "PACKAGE: $NAME"
echo "CURRENT VERSION: $LAST_VERSION"
echo "NEW VERSION: $VERSION"

python setup.py sdist bdist_wheel
twine upload --verbose dist/*
git tag -a v$VERSION -m "version $VERSION"
git push --tags
git push origin master
