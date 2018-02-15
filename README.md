````
# container start
./start.sh

# docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.6

# connect from host
mysql -u root -h 127.0.0.1
````

## Running Tests
````
env PYTHONPATH=$PYTHONPATH:$(pwd)/tubular python tests/crawl_test.py
````