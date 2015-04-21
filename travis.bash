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

check_all_files () {
    (IFS=' ';
    for file in $1;
    do
      check_file "$(echo -e "$file" | tr -d '[[:space:]]')"
    done)
}

echo "Checking for all files"

check_all_files "UML.pdf apiary.apib IDB.log tests.py tests.out config.py models.html README.md"

cd app/

check_file "models.py"
check_file "views.py"

cd templates/

check_all_files "
about.html funRunApi.html Index.html periodLayout.html tests.html elementLayout.html groupLayout.html layout.html tests_executor.html timeline.html"

cd ../static/css

check_all_files "elements.css  group.css  groups.css  index.css  periodic-table.css  reset.css  style.css"

cd ../scripts/ "carousel.js  jumbotron.js  main.js  modernizr.js  periodictable.js"

cd ../../../

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
git commit -m "$commit_message"
git push -f "https://github.com/josebigio/cs373-idb.git" origin travis-ci

echo "Done."