# Android application
Download ```MaDic-0.1-arm64-v8a_armeabi-v7a-debug (19).apk```

# Web application
## Environment variables
Set up environment variables in ```.env``` file.
See ```.example.env``` file for required variables.
If necessary, set up relevant variables in ```config.py``` file.

## Windows OS
If virtual environment doesn't exist already
```py
python -m venv .venv
```
Activate virtual environment

```bash
".venv\Scripts\activate"
```
Start flask app

```py
python app.py
```