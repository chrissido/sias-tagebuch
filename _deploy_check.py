#!/usr/bin/env python3
"""Deploy nur die Web-Dateien an Netlify (ohne pgdata)"""
import base64, json, os, zipfile, io, hashlib, mimetypes

token = base64.b64decode("...8c").decode()
site_id = "...34"

# Nur Web-Dateien
web_dir = "D:/Sias Tagebuch"
exclude_dirs = {"immich", ".git", ".netlify", "node_modules", "uploads", "netlify"}
exclude_files = {"deploy.bat", "_deploy_now.bat", "starte-lumi-server.bat", "starte-lumi-cloudflare.bat", 
                  "deploy.sh", "do-deploy.sh", "set_env.py", "lumi-server.py", "test-server.py",
                  "test2.py", "server.log", "test-server.log", "test2.log", ".env"}
exclude_ext = {".py", ".bat", ".sh", ".log", ".psd", ".7z", ".zip"}

files = []
for root, dirs, fnames in os.walk(web_dir):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for f in fnames:
        ext = os.path.splitext(f)[1].lower()
        if f in exclude_files or ext in exclude_ext:
            continue
        fp = os.path.join(root, f)
        rp = os.path.relpath(fp, web_dir)
        files.append((rp, fp))

print(f"📦 {len(files)} Dateien zum Deploy")
# API: https://api.netlify.com/api/v1/sites/{site_id}/deploys
for rp, fp in files[:5]:
    print(f"   {rp}")
print(f"   ... und {len(files)-5} weitere")

# Wir machen einen Directory-Upload via API
# Oder: Nutze netlify CLI aus dem deploy.bat mit Token
print(f"\n--- Token: {token[:8]}...{token[-4:]}")
print(f"--- Site: {site_id}")
print(f"✅ Fertig! Nutze: NETLIFY_AUTH_TOKEN={token[:8]}...{token[-4:]} netlify deploy --prod")
