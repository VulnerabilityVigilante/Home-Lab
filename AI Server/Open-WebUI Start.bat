@echo off
@echo Starting Open WebUI...

REM Set the path for the secret key file to a user-writable directory
set WEBUI_SECRET_KEY=C:\Users\{USERNAME}\.open-webui\webui_secret_key

REM Initialize Conda (adjust the path as needed)
call C:\Users\{USERNAME}\anaconda3\Scripts\activate.bat C:\Users\{USERNAME}\anaconda3

REM Launch a new minimized CMD window that activates the environment,
REM updates open-webui, and then starts the service
start "" /min cmd /K "conda activate open-webui && pip install --upgrade open-webui && open-webui serve"
