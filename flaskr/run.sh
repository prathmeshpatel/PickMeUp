#!/bin/sh
function usage() {
    echo "Usage: sh ${0} create.db"
}
export FLASK_APP=flaskr
export FLASK_DEBUG=true
if [ "$#" -ne 1 ]; then
    usage
    exit 1
fi
FILE=$1
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    echo "DB does not exist, initializing db."
    flask initdb
fi
flask run
