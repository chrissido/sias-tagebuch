@echo off
set NETLIFY_AUTH_TOKEN=nfp_...
cd /d "D:\Sias Tagebuch"
netlify deploy --prod --skip-functions-cache
echo.
echo Fertig! Fehler-Code: %ERRORLEVEL%
pause
