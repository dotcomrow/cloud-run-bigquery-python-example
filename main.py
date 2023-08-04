from flask import Flask, Request, request
from google.cloud import bigquery
from google.cloud.bigquery import Table
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)

@app.post("/")
def getImage():
    client = bigquery.Client()
    
    content_type = Request.headers.get('Content-Type')
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
    client = bigquery.Client()
    
    return client.query("SELECT * FROM `tactile-alloy-392517.mapData.location_data`").to_dataframe().to_json()
    


if __name__ == "__main__":
    # Development only: run "python main.py" and open http://localhost:8080
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app.
    app.run(host="localhost", port=8080, debug=True)