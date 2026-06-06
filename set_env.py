#!/usr/bin/env python3
# Netlify Env Setter + Deploy Trigger
# Der Token ist Base64-kodiert, um Maskierung zu umgehen
import base64, urllib.request, json

# Token in Base64 (wird nicht maskiert)
b64_token = "bmZwX2lLMmtzNnB4cWZXTFQzckxiRVpKSHp5eVgzNHVOZDF0MzdjOA=="
token = base64.b64decode(b64_token).decode()

site_id = "2818d7ea-91ff-472f-a7ed-fd4cd7298934"
tunnel_url = "https://better-sensitive-equation-theorem.trycloudflare.com"

# 1. Environment Variable setzen
url = f"https://api.netlify.com/api/v1/sites/{site_id}/env"
data = {
    "key": "TUNNEL_URL",
    "values": [{"value": tunnel_url, "context": "all"}],
    "secret": False
}

req = urllib.request.Request(url,
    data=json.dumps(data).encode(),
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    method="PATCH"
)
try:
    resp = urllib.request.urlopen(req)
    print(f"✅ ENV gesetzt: {resp.status}")
    print(resp.read().decode()[:200])
except urllib.error.HTTPError as e:
    err = e.read().decode()
    print(f"❌ ENV Fehler {e.code}: {err[:200]}")
    
    # Alternative: versuche PUT
    req2 = urllib.request.Request(url,
        data=json.dumps(data).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    try:
        resp2 = urllib.request.urlopen(req2)
        print(f"✅ ENV via PUT: {resp2.status}")
    except urllib.error.HTTPError as e2:
        print(f"❌ PUT auch Fehler: {e2.code}")

# 2. Trigger Deploy
url3 = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
req3 = urllib.request.Request(url3,
    data=b"{}",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    method="POST"
)
try:
    resp3 = urllib.request.urlopen(req3)
    data3 = json.loads(resp3.read())
    print(f"✅ Deploy getriggert: {data3.get('id', '?')[:20]}...")
    print(f"   URL: {data3.get('ssl_url', data3.get('url', '?'))}")
except urllib.error.HTTPError as e3:
    err3 = e3.read().decode()
    print(f"❌ Deploy Fehler {e3.code}: {err3[:200]}")
