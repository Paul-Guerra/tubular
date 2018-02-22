````
# container start
./start.sh

# initialize database
mysql -u root -h 127.0.0.1 < tubular/data_store/init.sql
````

Use mysql tools to create .mylogin.cnf
````
mysql_config_editor set --login-path=tubular --host=127.0.0.1 --user=tubular --password
````

now you can connect from host via
````
mysql --login-path=tubular
````

Initilize migrations
Edit alembic.ini to use the correct db DSN for the sqlalchemy url then run 
````
alembic upgrade head
````
## Running Tests
````
env PYTHONPATH=$PYTHONPATH:$(pwd)/tubular python tests/crawler/crawl_test.py
````

## Executing a service
````
env PYTHONPATH=$PYTHONPATH:$(pwd)/tubular python tubular/crawler/crawl.py
````