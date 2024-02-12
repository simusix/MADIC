
# Start
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

```py
".venv\Scripts\activate"
```
Start flask app

```py
python app.py
```