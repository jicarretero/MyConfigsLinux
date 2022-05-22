#!/bin/bash

cd $(dirname $0) 

source ~/.venv/krtpomodoro/bin/activate
( ./HttpBasicServer.py & )
