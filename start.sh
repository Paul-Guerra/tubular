#! /bin/bash
mkdir -p $(pwd)/volumes/mysql/data

HOST_MYSQL_DATA="$(pwd)/volumes/mysql/data"

[[ -e "./config.sh" ]] && source "./config.sh" 

docker run -ti --rm \
  -v $HOST_MYSQL_DATA:/var/lib/mysql \
  -e MYSQL_ALLOW_EMPTY_PASSWORD=yes \
  --name tubular_db \
  --v $(pwd)/data_store/.my.cnf: /root/.my.cnf \
  -p 3306:3306 \
  -d \
  mysql:5.6 
