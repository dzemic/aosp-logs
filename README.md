> **WARNING:** This code has been developed purely with AI. It has not been tested and may contain errors or vulnerabilities. It's for demo purposes only. Use at your own risk. Everything in this REPO is intended as a joke.

---


## How it works?

- Run your program in your terminal or tool or choice.
- Encounter dumb error.
- Run ENGINE, providing your VertexAI enabled GCP Project ID, Region and local code directory.
- Copy your error from terminal one into FIX-IT and type "eof" hit enter.
- Have code and error uploaded and then get AI generated response and possible (questionable) quality AI recommended fix.

## Setup & Run FIX-IT

> **NOTE:** You will need a Google Cloud project, with VertexAI API's enabled. Additionally the terminal in which you run FIX-IT will need to be authenticated to that Google Cloud project using the **gcloud** cli.

```
cd ./engine
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python main.py ../example-program --project_id "XXXX" --location "XXXXX"
```


## Example Program;

This is basically a folder you can ignore. It contains a python application that "works" and you can break it deliberately to create errors to pass to FIX-IT along side the code it self for demo/testing purposes.

You should replace the `../example-program` parameter when calling FIX-IT with your own path to your code directory.
