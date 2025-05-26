from flask import Flask
import os
import argparse
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig # Updated import for latest SDK

app = Flask(__name__)

@app.route("/")
def hello():
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    location = "us-central1"

    model_name = "gemini-2.0-flash-001"


    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)


    generation_config = GenerationConfig(
            temperature=0.2, # Lower temperature for more factual, less creative responses
            # max_output_tokens=2048, # Adjust as needed
        )



    prompt = f"""
        You are an expert debugging assistant
    """


    response = model.generate_content(
           [Part.from_text(prompt)],
           generation_config=generation_config,
           # safety_settings=... # Add safety settings if needed
        )


    #return f"Hello from Cloud Run! GCP_PROJECT_ID={project_id}\n"
    return response.text 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

