> **WARNING:** This code has been developed purely with AI. It has not been tested and may contain errors or vulnerabilities. It's for demo purposes only. Use at your own risk. Everything in this REPO is intended as a joke.

---

# FIX-IT

Literally one of the worst programs ever written. A dumb program (fix-it) for fixing dumb problems made by questionably dumb developers.

## How it works?

- Run your program in your terminal or tool or choice.
- Encounter dumb error.
- Run FIX-IT, providing your VertexAI enabled GCP Project ID, Region and local code directory.
- Copy your error from terminal one into FIX-IT and type "eof" hit enter.
- Have code and error uploaded and then get AI generated response and possible (questionable) quality AI recommended fix.

## Setup & Run FIX-IT

> **NOTE:** You will need a Google Cloud project, with VertexAI API's enabled. Additionally the terminal in which you run FIX-IT will need to be authenticated to that Google Cloud project using the **gcloud** cli.

```
cd ./fix-it
source venv/bin/activate
pip install -r requirements.txt

python main.py ../example-program --project_id "XXXX" --location "XXXXX"
```

## Aussie Mode;

Need responses that are specifically more blunt and direct? Maybe some of the harsh feedback you really need?
Run it in Aussie Mode! (-aussie_mode)

```
python main.py ../example-program --project_id "XXXX" --location "XXXXX" -aussie_mode
```

## Example Program;

This is basically a folder you can ignore. It contains a python application that "works" and you can break it deliberately to create errors to pass to FIX-IT along side the code it self for demo/testing purposes.

You should replace the `../example-program` parameter when calling FIX-IT with your own path to your code directory.
