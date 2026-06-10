@echo off
title 🌸 LUMI - Sias Tagebuch
echo ============================================
echo  🌸 LUMI - Sias Tagebuch Server
echo ============================================
echo.
echo  Starte Server...
echo.

:: Lokalen Server starten (im Hintergrund)
start /B "" python "D:\Sias Tagebuch\lumi-server.py"

:: Kurz warten
timeout /t 2 /nobreak >nul

:: Cloudflare Tunnel starten
echo  🌐 Cloudflare Tunnel wird gestartet...
echo  📡 Warte auf Verbindung...
echo.
echo  Deine öffentliche Adresse erscheint unten:
echo  ───────────────────────────────────────────
echo.

"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Cloudflare.cloudflared_Microsoft.Winget.Source_8wekyb3d8bbwe\cloudflared.exe" tunnel --url http://localhost:8899

echo.
echo  ⏹️  Tunnel geschlossen.
pause
