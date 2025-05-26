import os
import argparse
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig # Updated import for latest SDK
import mimetypes # For better language guessing (optional, can simplify)

# --- Configuration ---
# You can set these as environment variables or modify them here
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
GCP_LOCATION = os.environ.get("GCP_LOCATION", "us-central1") # e.g., us-central1
GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.0-flash-001") # or gemini-1.0-pro, gemini-1.5-pro etc.

# Files/directories to ignore
IGNORE_DIRS = ['.git', '__pycache__', 'node_modules', 'venv', '.venv', 'env', '.env', 'build', 'dist', 'target']
IGNORE_FILES = ['.DS_Store']
# Focus on text-based source files and common configs
# Add or remove extensions as needed
INCLUDE_EXTENSIONS = [
    '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss', '.java', '.c', '.cpp', '.h', '.hpp',
    '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.ini', '.toml', '.sh', '.rb', '.go', '.php',
    '.sql', 'Dockerfile', '.dockerignore', '.gitignore', '.tf', '.tfvars', '.conf', '.cfg', '.log'
]
MAX_FILE_SIZE_BYTES = 1 * 1024 * 1024  # 1 MB limit per file to avoid overly large contexts

def get_markdown_language_tag(filepath):
    """Guess the language for Markdown code block based on extension."""
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    mapping = {
        '.py': 'python', '.js': 'javascript', '.jsx': 'javascript', '.ts': 'typescript',
        '.tsx': 'typescript', '.html': 'html', '.css': 'css', '.scss': 'scss',
        '.java': 'java', '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.hpp': 'cpp',
        '.md': 'markdown', '.json': 'json', '.yaml': 'yaml', '.yml': 'yaml',
        '.xml': 'xml', '.sh': 'bash', '.rb': 'ruby', '.go': 'go', '.php': 'php',
        '.sql': 'sql', 'dockerfile': 'dockerfile', '.tf': 'hcl', '.tfvars': 'hcl',
        '.log': 'log', '.txt': '' # No language tag for plain text
    }
    # Handle files with no extension but known names (e.g., Dockerfile)
    basename = os.path.basename(filepath).lower()
    if basename in mapping:
        return mapping[basename]
    return mapping.get(ext, '') # Default to no language tag if unknown

def package_code_to_markdown(directory_path):
    """
    Packages up source code and files within the directory into Markdown format.
    Simulates a basic "REPOMIX" functionality.
    """
    markdown_output = []
    abs_directory_path = os.path.abspath(directory_path)
    markdown_output.append(f"# Code and Files from: {abs_directory_path}\n\n")

    for root, dirs, files in os.walk(abs_directory_path, topdown=True):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for filename in files:
            if filename in IGNORE_FILES:
                continue

            # Check if the file extension (or full name for extensionless) is in INCLUDE_EXTENSIONS
            _, ext = os.path.splitext(filename)
            is_included = (ext.lower() in INCLUDE_EXTENSIONS or
                           filename in INCLUDE_EXTENSIONS) # For files like 'Dockerfile'

            if not is_included:
                continue

            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, abs_directory_path)

            try:
                # Check file size
                if os.path.getsize(file_path) > MAX_FILE_SIZE_BYTES:
                    markdown_output.append(f"## File: {relative_path}\n")
                    markdown_output.append(f"*Note: File skipped as it exceeds {MAX_FILE_SIZE_BYTES // 1024 // 1024}MB limit.*\n\n")
                    continue

                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                lang_tag = get_markdown_language_tag(filename)
                markdown_output.append(f"## File: {relative_path}\n")
                markdown_output.append(f"```{lang_tag}\n")
                markdown_output.append(content.strip())
                markdown_output.append("\n```\n\n")
            except Exception as e:
                markdown_output.append(f"## File: {relative_path}\n")
                markdown_output.append(f"*Error reading file: {e}*\n\n")

    return "".join(markdown_output)

def get_terminal_logs():
    """Prompts the user to paste their terminal stdout and stderr."""
    print("\n--- Please paste your latest terminal stdout and stderr ---")
    print("--- Type 'EOF' (or Ctrl-D/Ctrl-Z then Enter) on a new line when done ---")
    logs = []
    while True:
        try:
            line = input()
            if line.strip().upper() == "EOF": # Manual EOF marker
                break
            logs.append(line)
        except EOFError: # Ctrl-D (Unix) or Ctrl-Z then Enter (Windows)
            break
    return "\n".join(logs)

def analyze_with_gemini(project_id, location, model_name, code_markdown, terminal_logs):
    """
    Sends the combined code and logs to Gemini via Vertex AI for analysis.
    """
    if not project_id or project_id == "your-gcp-project-id":
        print("ERROR: GCP_PROJECT_ID is not set. Please set it or pass as an argument.")
        return "Error: GCP Project ID not configured."

    try:
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel(model_name)
        
        prompt = f"""
    You are an expert debugging assistant. I will provide you with a collection of source code files from a project and the latest terminal output (stdout/stderr).

    Your tasks are:
    1.  **Error/Log Assessment:** Identify any errors, warnings, or unusual patterns in the terminal logs.
    2.  **Explanation:** Clearly explain what these errors/logs mean in the context of the provided code.
    3.  **Possible Code Modifications:** Suggest specific code modifications (with file paths if possible) that could fix the identified issues or improve the situation. If no clear errors are present, analyze the logs for potential improvements or areas of concern.
    4.  **Be concise and actionable.**

    Here is the packaged source code:
    <CODE_PACKAGE>
    {code_markdown}
    </CODE_PACKAGE>

    Here are the terminal logs (stdout/stderr):
    <TERMINAL_LOGS>
    {terminal_logs}
    </TERMINAL_LOGS>

    Please provide your analysis:
    """
        # Using GenerationConfig for more control if needed, like temperature
        generation_config = GenerationConfig(
            temperature=0.2, # Lower temperature for more factual, less creative responses
            # max_output_tokens=2048, # Adjust as needed
        )

        print("\nSending data to Gemini for analysis... This may take a moment.")
        response = model.generate_content(
            [Part.from_text(prompt)],
            generation_config=generation_config,
            # safety_settings=... # Add safety settings if needed
        )

        return response.text

    except Exception as e:
        print(f"An error occurred while interacting with Vertex AI: {e}")
        # You might want to print more details from e, like e.args
        return f"Error during Gemini analysis: {e}"


def main():
    parser = argparse.ArgumentParser(description="Package code, get logs, and send to Gemini for analysis.")
    parser.add_argument("directory", help="The directory containing the source code to package.")
    parser.add_argument("--project_id", default=GCP_PROJECT_ID, help="Google Cloud Project ID.")
    parser.add_argument("--location", default=GCP_LOCATION, help="Google Cloud Location (e.g., us-central1).")
    parser.add_argument("--model", default=GEMINI_MODEL_NAME, help="Gemini model name (e.g., gemini-2.0-flash-001).")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
        return

    print(f"Packaging code from: {args.directory}")
    code_markdown = package_code_to_markdown(args.directory)
    # print("\n--- Packaged Code (Markdown Preview) ---")
    # print(code_markdown[:1000] + "\n..." if len(code_markdown) > 1000 else code_markdown) # Preview

    terminal_logs = get_terminal_logs()
    # print("\n--- Captured Logs ---")
    # print(terminal_logs)

    if not code_markdown.strip() and not terminal_logs.strip():
        print("No code or logs to analyze. Exiting.")
        return
    elif not code_markdown.strip():
        print("Warning: No code files were packaged. Analysis will be based on logs only.")
    elif not terminal_logs.strip():
        print("Warning: No terminal logs provided. Analysis will be based on code only.")


    print(f"\nUsing Project ID: {args.project_id}, Location: {args.location}, Model: {args.model}")
    analysis_result = analyze_with_gemini(args.project_id, args.location, args.model, code_markdown, terminal_logs)

    print("\n--- Gemini Analysis ---")
    print(analysis_result)
    print("--- End of Analysis ---")

if __name__ == "__main__":
    main()