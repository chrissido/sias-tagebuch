@echo off
set NETLIFY_AUTH_TOKEN=nfp_RDQAKsExYXexENXFc3N5xMeeT6fno4d64507
cd /d "D:\Sias Tagebuch"
netlify deploy --prod --skip-functions-cache
echo.
echo Fertig! Fehler-Code: %ERRORLEVEL%
pause
