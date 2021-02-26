# Scriba Custom Events

Scriba Custom Evants (or SCE) is an additional tool for [Scriba Bot](https://github.com/ScribaSSU).

# How to start server

## Start on localhost

### Flask only

The method should work on any platform.

1. Move into the project root directory:

```bash
cd <directory_with_projects>/scriba-custom-events
```

2. Start a local server with `python` (or `python3` if you have both python 
   versions 2 and 3) command and `app.py` module:
   
```bash
python app.py
```

3. Open http://127.0.0.1:5000 into your browser and use SCE.

### Flask + Gunicorn

**NOTE**: The method works **only** on UNIX OS. Gunicorn doesn't work on Windows.

1. Move into the project root directory:

```bash
cd <directory_with_projects>/scriba-custom-events
```

2. Start a local server with follow command
   
```bash
SCRIPT_NAME=/sce gunicorn -w 4 -b 127.0.0.1:5000 app_var:app
```

where `SCRIPT_NAME` is an environmental variable which allow use application paths 
with the permanent prefix (`/sce` in this case).
Option `-w N` runs application on `N` working processes.
Option `-b <ip_address>:<port>` specifies address and port for application 
(default value for Gunicorn is `127.0.0.1:8000`).

3. Open http://localhost:5000/sce into your browser and use SCE.
