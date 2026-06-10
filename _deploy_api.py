#!/usr/bin/env python3
"""Trigger Netlify Deploy per API"""
import base64, json, urllib.request

token = base64.b64decode("***8c").decode()
site_id = "2818d7ea-91ff-472f-a7ed-fd4cd7298934"

# Check token validity first
url = f"https://api.netlify.com/api/v1/sites/{site_id}"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    print(f"✅ Token OK - Site: {data.get('name', '?')}")
except Exception as e:
    print(f"❌ Token Fehler: {e}")
    exit(1)

# Trigger new deploy from local path
# We upload files directly
import os, hashlib, mimetypes

web_dir = "D:/Sias Tagebuch/_site"
exclude_dirs = {"immich", ".git", "pgdata", "pgdata_bak", "node_modules"}

files = []
for root, dirs, fnames in os.walk(web_dir):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for f in fnames:
        fp = os.path.join(root, f)
        rp = os.path.relpath(fp, web_dir).replace("\\", "/")
        if os.path.getsize(fp) == 0:
            continue
        files.append((rp, fp))

print(f"📦 {len(files)} Dateien hochladen...")

# Create deploy
deploy_url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
req = urllib.request.Request(deploy_url,
    data=b"{}",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST")
resp = json.loads(urllib.request.urlopen(req).read())
deploy_id = resp["id"]
required = resp.get("required", [])
print(f"✅ Deploy {deploy_id} created")

# Upload files
uploaded = 0
for rp, fp in files:
    if required and rp not in required:
        continue
    with open(fp, "rb") as fh:
        data = fh.read()
    mime = mimetypes.guess_type(fp)[0] or "application/octet-stream"
    sha = hashlib.sha256(data).hexdigest()
    
    file_url = f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{rp}"
    req2 = urllib.request.Request(file_url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": mime
        },
        method="PUT")
    try:
        urllib.request.urlopen(req2)
        uploaded += 1
        if uploaded % 20 == 0:
            print(f"   ... {uploaded}/{len(files)} hochgeladen")
    except Exception as e:
        print(f"   ❌ {rp}: {e}")

print(f"\n🎉 {uploaded} Dateien hochgeladen!")
print(f"🌐 https://sias-tagebuch.netlify.app")
