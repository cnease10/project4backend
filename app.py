from flask import Flask, jsonify, g
from flask_cors import CORS 

import models
from resources.dates import date

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
app = Flask(__name__)

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


#supports_credentials = true means we allow cookies to be sent to the server
CORS(date, origins=['http://localhost:3000'], supports_credentials=True) 
app.register_blueprint(date,  url_prefix='/api/v1/dates') 

# Run the app 
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)