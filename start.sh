#!/bin/bash
python3 ./flask/app.py &
yarn dev --host=0.0.0.0
