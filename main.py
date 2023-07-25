from io import BytesIO
import io
from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)

@app.post("/")
def getImage():
    
    return "Hello World!"


if __name__ == "__main__":
    # Development only: run "python main.py" and open http://localhost:8080
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app.
    app.run(host="localhost", port=8080, debug=True)