#!/bin/bash
redis-server &
python3 ./flask/app.py &
yarn dev
