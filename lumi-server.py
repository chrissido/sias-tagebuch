#!/usr/bin/env python3
"""
LUMI Server – Einfach + Upload
================================
Verhält sich bei GET/HEAD exakt wie python -m http.server.
Zusätzlich: POST /upload für Datei-Uploads.
"""
import http.server
import json, os, base64, uuid, socketserver
from datetime import datetime

PORT = 9999
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
META_FILE = os.path.join(UPLOAD_DIR, "_metadata.json")

ALLOWED_EXT = {'.jpg','.jpeg','.png','.gif','.webp','.mp4','.mov','.webm','.mp3','.ogg','.wav','.m4a','.heic','.heif'}
MAX_SIZE = 10 * 1024 * 1024

class LUMIHandler(http.server.SimpleHTTPRequestHandler):
    """Erweitert SimpleHTTPRequestHandler um POST /upload"""

    def do_POST(self):
        if self.path != '/upload':
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error":"Nicht gefunden"}')
            return

        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length).decode('utf-8'))
            files = body.get('files', [])
            if not files:
                self._json(400, {'error': 'Keine Dateien'})
                return

            uploader = body.get('uploader', 'Familie')
            global_description = body.get('description', '')
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            metadata = []
            if os.path.exists(META_FILE):
                with open(META_FILE, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

            results = []
            for f in files:
                name = f.get('name', '')
                data_b64 = f.get('data', '')
                if not data_b64:
                    results.append({'filename': name, 'status': 'error', 'error': 'Keine Daten'})
                    continue
                raw = base64.b64decode(data_b64)
                if len(raw) > MAX_SIZE:
                    results.append({'filename': name, 'status': 'error', 'error': 'Zu gro\u00df (max 10 MB)'})
                    continue
                ext = os.path.splitext(name)[1].lower()
                if ext not in ALLOWED_EXT:
                    results.append({'filename': name, 'status': 'error', 'error': f'{ext} nicht erlaubt'})
                    continue
                file_id = str(uuid.uuid4())
                safe_name = f"{file_id}{ext}"
                filepath = os.path.join(UPLOAD_DIR, safe_name)
                with open(filepath, 'wb') as out:
                    out.write(raw)
                file_desc = f.get('description', '') or global_description
                entry = {
                    'id': file_id, 'filename': name, 'savedAs': safe_name,
                    'filepath': filepath, 'size': len(raw),
                    'uploadDate': datetime.now().isoformat(),
                    'uploader': uploader, 'description': file_desc, 'status': 'pending',
                }
                metadata.append(entry)
                results.append({'filename': name, 'status': 'success'})

            with open(META_FILE, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            success = sum(1 for r in results if r['status'] == 'success')
            self._json(200, {'message': f'{success} Datei(en) gespeichert', 'results': results})

        except Exception as e:
            self._json(500, {'error': str(e)})

    def _json(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

if __name__ == '__main__':
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    print(f"\n🌸 LUMI auf Port {PORT}")
    print(f"   GET  = {PORT} (wie python -m http.server)")
    print(f"   POST /upload = Dateien speichern")
    print(f"   http://192.168.2.35:{PORT}/\n")
    with socketserver.ThreadingTCPServer(('', PORT), LUMIHandler) as server:
        server.allow_reuse_address = True
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Gestoppt.")
