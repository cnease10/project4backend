from flask import Flask, jsonify, g
from flask_cors import CORS 
from flask_login import LoginManager


import models
#import resources
from resources.dates import date
from resources.users import user
from resources.creates import create

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
app = Flask(__name__)

app.secret_key = "ladedaladeda" #secret key encodes session
login_manager = LoginManager()
login_manager.init_app(app) #sets up sessions

@login_manager.user_loader #loads user object when we access the session
#grab user by importing current_user from flask_login
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except: models.DoesNotExist
    return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


CORS(app, origins=['http://localhost:3000'], supports_credentials=True) 
#supports_credentials = true means we allow cookies to be sent to the server
CORS(date, origins=['http://localhost:3000'], supports_credentials=True) 
app.register_blueprint(date,  url_prefix='/api/v1/dates') 
CORS(user, origins=['http://localhost:3000'], supports_credentials=True) 
app.register_blueprint(user,  url_prefix='/api/v1/users') 
CORS(create, origins=['http://localhost:3000'], supports_credentials=True) 
app.register_blueprint(create,  url_prefix='/api/v1/creates') 

# Run the app 
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)