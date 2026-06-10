#!/usr/bin/env python3
"""Batch face recognition - uses recognize_faces.py's recognize function."""
import json
import os
import sys

BASE_DIR = "D:/Sias Tagebuch"
MOMENTE_FILE = os.path.join(BASE_DIR, "momente.json")
RESULTS_FILE = os.path.join(BASE_DIR, "face_scan_results.json")

# Importiere die recognize-Funktion
sys.path.insert(0, BASE_DIR)
from recognize_faces import recognize

def main():
    with open(MOMENTE_FILE, "r", encoding="utf-8") as f:
        momente = json.load(f)
    
    results = {}
    total = len(momente)
    
    for i, entry in enumerate(momente):
        eid = entry["id"]
        bild = entry.get("bild")
        
        if not bild or bild == "null":
            results[eid] = {"status": "no_image", "faces": []}
            continue
        
        abs_path = os.path.join(BASE_DIR, bild)
        if not os.path.exists(abs_path):
            results[eid] = {"status": "file_missing", "faces": []}
            print(f"[{i+1}/{total}] ID {eid}: {bild} ❌ Datei fehlt")
            continue
        
        print(f"[{i+1}/{total}] ID {eid}: {bild} ... ", end="", flush=True)
        faces = recognize(abs_path)
        
        if faces:
            names = [f["person"] for f in faces]
            confs = [f["confidence"] for f in faces]
            results[eid] = {
                "status": "ok",
                "faces": faces,
                "count": len(faces),
                "names": names,
            }
            print(f"✅ {names} (conf={confs})")
        else:
            results[eid] = {"status": "no_faces_detected", "faces": []}
            print(f"⚠️ Keine Gesichter erkannt")
    
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Ergebnisse gespeichert: {RESULTS_FILE}")

if __name__ == "__main__":
    main()
