#!/bin/bash
DIR=venv
REQ=requirements.txt
if [ ! -d "./$DIR" ]; then
    virtualenv $DIR
    . $DIR/bin/activate
    pip install -r $REQ
fi
