````
# container start
./start.sh

# connect from host
mysql -u root -h 127.0.0.1

CREATE DATABASE tubular;

# create an app user and migrate user
GRANT ALL PRIVILEGES ON tubular.* TO 'tubular_migrate'@'%' IDENTIFIED BY 'INSERT PASSWORD HERE';
GRANT SELECT ON tubular.* TO 'tubular'@'%' IDENTIFIED BY 'INSERT PASSWORD HERE';
GRANT INSERT ON tubular.* TO 'tubular'@'%' IDENTIFIED BY 'INSERT PASSWORD HERE';
GRANT UPDATE ON tubular.* TO 'tubular'@'%' IDENTIFIED BY 'INSERT PASSWORD HERE';
GRANT DELETE ON tubular.* TO 'tubular'@'%' IDENTIFIED BY 'INSERT PASSWORD HERE';
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
env PYTHONPATH=$PYTHONPATH:$(pwd)/tubular python tests/crawl_test.py
````