from flask import Flask
'''
To run via command line
FLASK_APP=server.py flask run
'''
app = Flask(__name__)
@app.route('/')
def hello_world():

    return 'Hello, World!'