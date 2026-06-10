#!/usr/bin/env python3
"""Deploy nur index.html an Netlify"""
import json, os, hashlib, urllib.request, mimetypes

# Token aus deploy.bat lesen (dort ist er un-maskiert)
with open("D:/Sias Tagebuch/deploy.bat") as f:
    for line in f:
        if "NETLIFY_AUTH_TOKEN" in line:
            token = line.split("=", 1)[1].strip()
            break

site_id = "2818d7ea-91ff-472f-a7ed-fd4cd7298934"
html_file = "D:/Sias Tagebuch/index.html"

# 1. Deploy erstellen
deploy_url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
req = urllib.request.Request(deploy_url,
    data=b"{}",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST")
resp = json.loads(urllib.request.urlopen(req).read())
deploy_id = resp["id"]
print(f"✅ Deploy {deploy_id[:20]}... erstellt")

# 2. index.html hochladen
with open(html_file, "rb") as f:
    data = f.read()

file_url = f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/index.html"
req2 = urllib.request.Request(file_url,
    data=data,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "text/html; charset=utf-8"
    },
    method="PUT")
resp2 = urllib.request.urlopen(req2)
print(f"✅ index.html hochgeladen ({len(data)} Bytes)")

# 3. CSS-Dateien auch hochladen
import glob
css_dir = "D:/Sias Tagebuch/assets/css"
for css_file in glob.glob(css_dir + "/*.css"):
    with open(css_file, "rb") as f:
        cdata = f.read()
    rp = os.path.relpath(css_file, "D:/Sias Tagebuch").replace("\\", "/")
    furl = f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{rp}"
    req3 = urllib.request.Request(furl,
        data=cdata,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "text/css"},
        method="PUT")
    urllib.request.urlopen(req3)
    print(f"✅ {rp} hochgeladen ({len(cdata)} Bytes)")

# 4. JS-Dateien
js_dir = "D:/Sias Tagebuch/assets/js"
for js_file in glob.glob(js_dir + "/*.js"):
    with open(js_file, "rb") as f:
        jdata = f.read()
    rp = os.path.relpath(js_file, "D:/Sias Tagebuch").replace("\\", "/")
    furl = f"https://api.netlify.com/api/v1/deploys/{deploy_id}/files/{rp}"
    req4 = urllib.request.Request(furl,
        data=jdata,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/javascript"},
        method="PUT")
    urllib.request.urlopen(req4)
    print(f"✅ {rp} hochgeladen ({len(jdata)} Bytes)")

# 5. Deploy publishen
publish_url = f"https://api.netlify.com/api/v1/deploys/{deploy_id}"
req5 = urllib.request.Request(publish_url,
    data=b'{"draft": false}',
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="PUT")
resp5 = urllib.request.urlopen(req5)
print(f"\n🎉 Fertig! https://sias-tagebuch.netlify.app")
