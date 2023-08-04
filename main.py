from flask import Flask, redirect, request, session, url_for
from google.cloud import bigquery
from google.cloud.bigquery import Table
from authlib.integrations.flask_client import OAuth
import google.cloud.logging
import logging

app = Flask(__name__)
logClient = google.cloud.logging.Client()
app.secret_key = '!secret'
app.config.from_object('config')

logClient.setup_logging()
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.post("/")
def getImage():
    try:
        token = oauth.google.authorize_access_token()
        if token is None:
            redirect_uri = url_for('/', _external=True, method='POST')
            return oauth.google.authorize_redirect(redirect_uri)
    except Exception as e: 
        logging.error(e, exc_info=True)
        return "Error"
    client = bigquery.Client()
    
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        
        table_id = Table.from_string("tactile-alloy-392517.mapData.location_data")
        rows_to_insert = [json]
        errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
        
        if errors == []:
            return "New rows have been added."
        else:
            return "Error"
    else:
        return 'Content-Type not supported!'
    

@app.get("/")
def getItems():
    try:
        token = oauth.google.authorize_access_token()
        if token is None:
            redirect_uri = url_for('/', _external=True, method='POST')
            return oauth.google.authorize_redirect(redirect_uri)
    except Exception as e: 
        logging.error(e, exc_info=True)
        return "Error"
    
    client = bigquery.Client()
    
    return client.query("SELECT * FROM `tactile-alloy-392517.mapData.location_data`").to_dataframe().to_json()
    


if __name__ == "__main__":
    # Development only: run "python main.py" and open http://localhost:8080
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app.
    app.run(host="localhost", port=8080, debug=True)