from flask import Flask
import os
import argparse
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig # Updated import for latest SDK

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Cloud Run (Python)!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

