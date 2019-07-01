
ps -ef | grep web.py | awk '{print $2}' | xargs kill -9
python3.6 ./web.py