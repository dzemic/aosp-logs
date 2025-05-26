from flask import Flask, request, jsonify
import os
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig

app = Flask(__name__)

@app.route("/", methods=["POST"])
def hello():
    # Expecting JSON with key "file_base64"
    data = request.get_json()
    if not data or "file_base64" not in data:
        return jsonify({"error": "Missing 'file_base64' in request body"}), 400

    try:
        decoded_bytes = base64.b64decode(data["file_base64"])
        content = decoded_bytes.decode("utf-8")
    except Exception as e:
        return jsonify({"error": f"Failed to decode base64: {str(e)}"}), 400

    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    location = "us-central1"
    model_name = "gemini-2.0-flash-001"

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)

    generation_config = GenerationConfig(temperature=0.2)

    prompt = f"""
    Analyse content of this, and provide feedback:
    {content}
    """

    response = model.generate_content(
        [Part.from_text(prompt)],
        generation_config=generation_config,
    )

    return response.text
