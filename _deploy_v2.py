#!/usr/bin/env python3
"""Deploy nur Web-Dateien an Netlify"""
import base64, os, json, urllib.request, hashlib, mimetypes, time

token = base64.b64decode("***8c").decode()
site_id = "2818d7ea-91ff-472f-a7ed-fd4cd7298934"

web_dir = "D:/Sias Tagebuch/_site"
exclude_dirs = {"immich", ".git", ".netlify", "uploads", "pgdata", "pgdata_bak"}
exclude_files = {".env", "*.py", "*.bat", "*.sh", "*.log", "*.7z"}

def get_files():
    files = []
    for root, dirs, fnames in os.walk(web_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in fnames:
            fp = os.path.join(root, f)
            rp = os.path.relpath(fp, web_dir).replace("\\", "/")
            files.append((rp, fp))
    return sorted(files)

files = get_files()
print(f"📦 {len(files)} Dateien")

# 1. Deploy erstellen
deploy_url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
req = urllib.request.Request(deploy_url, 
    data=b"{}",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST")
resp = json.loads(urllib.request.urlopen(req).read())
deploy_id = resp["id"]
require_upload = resp.get("required", [])
print(f"✅ Deploy {deploy_id[:20]}... erstellt")
print(f"📤 {len(require_upload)} Dateien müssen hochgeladen werden")

# 2. Dateien hashen und hochladen
upload_url = f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files"
for rp, fp in files:
    sha = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    print(f"   Check: {rp} -> {sha[:16]}...")
    if rp in require_upload or not require_upload:
        # Hochladen
        with open(fp, "rb") as fh:
            data = fh.read()
        mime = mimetypes.guess_type(fp)[0] or "application/octet-stream"
        req2 = urllib.request.Request(f"{upload_url}/{rp}",
            data=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": mime
            },
            method="PUT")
        try:
            urllib.request.urlopen(req2)
            print(f"   ✅ {rp}")
        except Exception as e:
            print(f"   ❌ {rp}: {e}")

print(f"\n🎉 Fertig! https://sias-tagebuch.netlify.app")
