from flask import Flask, redirect, request, session, url_for
from google.cloud import bigquery
from google.cloud.bigquery import Table
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

app.secret_key = '!secret'
app.config.from_object('config')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    return redirect('/')


@app.route('/logout')
def logout():
    return redirect('/')

@app.post("/")
def getImage():
    token = oauth.google.authorize_access_token()
    if token is None:
        redirect_uri = url_for('login', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)
    
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
    token = oauth.google.authorize_access_token()
    if token is None:
        redirect_uri = url_for('login', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)
    
    client = bigquery.Client()
    
    return client.query("SELECT * FROM `tactile-alloy-392517.mapData.location_data`").to_dataframe().to_json()
    


if __name__ == "__main__":
    # Development only: run "python main.py" and open http://localhost:8080
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app.
    app.run(host="localhost", port=8080, debug=True)