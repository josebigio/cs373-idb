#!/bin/bash

check_file () {
    if [ -f "$1" ]
    then
        echo "$1 found"
    else
        echo "$1 not found"
        exit -1
    fi
}

echo "Checking for all files"

check_file "UML.pdf"
check_file "apiary.apib"
check_file "IDB.log"
check_file "tests.py"
check_file "tests.out"

echo "Running tests"

coverage run tests.py 2> tests.out
coverage report -m app/*.py >> tests.out

echo "Making IDB.log"

commit_message=`git log -1 --pretty=%B`
commit_author=`git log -1 --pretty=%cn`
commit_email=`git log -1 --pretty=%ce`

git config --global user.name "$commit_author"
git config --global user.email "$commit_email"
git config --global push.default simple
git config --global credential.helper store
echo "https://${GITHUB_KEY}:x-oauth-basic@github.com" >> ~/.git-credentials

git checkout travis-ci
git log > IDB.log
git add -A
#git commit -m "Added IDB.log (Travis CI)"
#git reset --soft HEAD~1
git commit -m "$commit_message"
git push -f "https://github.com/josebigio/cs373-idb.git" HEAD:travis-ci

echo "Done."