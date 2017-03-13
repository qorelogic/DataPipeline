#!/bin/bash

genSpider() {
    if [ "$1" == "" ] || [ "$2" == "" ] || [ "$3" == "" ] || [ "$4" == "" ]; then
        echo "usage <name> <domain> <url> <item>"
    else
        url="$3"
        #url=`python -c "print '$3'.replace('/', '\/')"`
        #python -c "print '$url'.replace('\\\', '\\\\\\\')"
        #url='`echo "$3" | perl -pe "s/\//\\\//g"`'
        #echo $url

        cat template.py.tpl         | \
        perl -pe "s/{{name}}/$1/g"   | \
        perl -pe "s/{{domain}}/$2/g" | \
        #perl -pe "s/{{url}}/$url/"  | \
        python -c "import sys; print sys.stdin.read().replace('{{url}}', '$url')" | \
        perl -pe "s/{{item}}/$4/g" > numbeo/spiders/$1.py

        cat item.py.tpl         | \
        perl -pe "s/{{item}}/$4/g" >> numbeo/items.py
    fi
}
