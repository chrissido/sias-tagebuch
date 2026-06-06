@echo off
cd /d "D:\Sias Tagebuch"
set NETLIFY_AUTH_TOKEN=***
netlify deploy --prod --skip-functions-cache
echo.
echo Fertig!
