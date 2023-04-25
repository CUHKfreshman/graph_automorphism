#!/bin/bash
 npm run dev &
redis-server &
python3 ./flask/app.py 
