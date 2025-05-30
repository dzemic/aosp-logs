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
        mood = data["mood"]
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
    You are an {mood} expert debugging assistant. I will provide you with a collection of source code files from a project and the latest terminal output (stdout/stderr).
    Your tasks are:
    1.  **Error/Log Assessment:** Identify any errors, warnings, or unusual patterns in the terminal logs.
    2.  **Explanation:** Clearly explain what these errors/logs mean in the context of the provided code.
    3.  **Possible Code Modifications:** Suggest specific code modifications (with file paths if possible) that could fix the identified issues or improve the situation. If no clear errors are present, analyze the logs for potential improvements or areas of concern.
    4.  **Be concise and actionable.**
    Here is the packaged source code:
    {content}
    """

    response = model.generate_content(
        [Part.from_text(prompt)],
        generation_config=generation_config,
    )

    return response.text

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
