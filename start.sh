#!/bin/bash
 npm run dev &
redis-server &
python3 app.py 
