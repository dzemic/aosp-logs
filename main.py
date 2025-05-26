from flask import Flask, request
import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

app = Flask(__name__)

@app.route("/", methods=["POST"])
def hello():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    content = file.read().decode("utf-8")

    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    location = "us-central1"
    model_name = "gemini-2.0-flash-001"

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)

    generation_config = GenerationConfig(temperature=0.2)

    prompt = f"""
    Analayse content of this, and provide feedback:
    {content}
    """

    response = model.generate_content(
        [Part.from_text(prompt)],
        generation_config=generation_config,
    )

    return response.text
