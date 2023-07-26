from io import BytesIO
import io
from flask import Flask, request
from google.cloud import bigquery
from google.cloud.bigquery import Table

app = Flask(__name__)

@app.post("/")
def getImage():
    client = bigquery.Client()
    
    table_id = Table.from_string("tactile-alloy-392517.mapData.location_data")
    rows_to_insert = [
        {"location": "LINESTRING(-118 33, -73 40)", "description":"a test line"}
    ]
    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    
    if errors == []:
        return "New rows have been added."
    else:
        return "Success!"


if __name__ == "__main__":
    # Development only: run "python main.py" and open http://localhost:8080
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app.
    app.run(host="localhost", port=8080, debug=True)