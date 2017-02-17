#! /usr/bin/env bash

# This script is the entry point for the Travis tests platform.
# It first checks that the package version has been updated ("bump" in the jargon),
# then it runs tests via "make test", and tests the CLI.


set -x

current_version=`python setup.py --version`

if ! git diff-index --quiet master openfisca_web_api
then
    if [[ "$TRAVIS_BRANCH" == "master" && "$TRAVIS_PULL_REQUEST" != false ]]
    then
        if git rev-parse $current_version
        then
            set +x
            echo "Version $version already exists. Please update version number in setup.py before merging this branch into master."
            exit 1
        fi

        if git diff-index master --quiet CHANGELOG.md
        then
            set +x
            echo "CHANGELOG.md has not been modified. Please update it before merging this branch into master."
            exit 1
        fi
    fi
fi

make test

bash openfisca_web_api/tests/test-cli.sh
