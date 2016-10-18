#!/bin/bash

echo "Waiting for mysql"
until mysql -hdb -uroot -proot -e ';' weather
do
  printf "."
  sleep 1
done

echo -e "\nmysql ready"

python3 weather_snowpack_website/manage.py migrate
python3 weather_snowpack_website/manage.py initadmin
python3 weather_snowpack_website/manage.py runserver 0.0.0.0:8000
while true; do sleep 1d; done
echo -e "\nhttp-server ready"