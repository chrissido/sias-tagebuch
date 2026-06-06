// upload.mjs – LUMI Upload (Netlify Blobs)
// Familie lädt hoch → Datei landet in Netlify Blobs
// LUMI holt sie später ab, beschreibt sie und löscht sie

import { getStore } from "@netlify/blobs";

const MAX_SIZE = 25 * 1024 * 1024; // 25 MB (Blobs Limit Free Plan)
const ALLOWED = ["jpg","jpeg","png","gif","webp","mp4","mov","webm","mp3","ogg","wav","m4a","heic","heif"];

function classify(name) {
  const ext = name.split(".").pop()?.toLowerCase();
  if (["jpg","jpeg","png","gif","webp","heic","heif"].includes(ext)) return { type: "Bild", icon: "📸" };
  if (["mp4","mov","webm"].includes(ext)) return { type: "Video", icon: "🎬" };
  if (["mp3","ogg","wav","m4a"].includes(ext)) return { type: "Audio", icon: "🎤" };
  return { type: "Datei", icon: "📄" };
}

const headers = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json"
};

const STORE_NAME = "lumi-uploads";

export const handler = async (event) => {
  // CORS Preflight
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers, body: "" };
  }

  try {
    const store = getStore(STORE_NAME);

    // === GET: Neue Uploads abholen (für LUMI) ===
    if (event.httpMethod === "GET") {
      const { blobs } = await store.list();
      
      const uploads = [];
      for (const blob of blobs) {
        const meta = blob.metadata || {};
        const data = await store.get(blob.key, { type: "text" });
        uploads.push({
          key: blob.key,
          filename: meta.filename || blob.key,
          type: meta.type || "Datei",
          icon: meta.icon || "📄",
          uploader: meta.uploader || "Familie",
          description: meta.description || "",
          uploadedAt: blob.uploadedAt || meta.uploadedAt,
          size: meta.size || 0,
          data: data // Base64
        });
      }

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ uploads })
      };
    }

    // === DELETE: Upload löschen (nach Verarbeitung durch LUMI) ===
    if (event.httpMethod === "DELETE") {
      const body = JSON.parse(event.body || "{}");
      const keys = body.keys || [];
      
      let deleted = 0;
      for (const key of keys) {
        try {
          await store.delete(key);
          deleted++;
        } catch (e) {
          console.log(`Fehler beim Löschen von ${key}: ${e.message}`);
        }
      }

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ deleted, message: `${deleted} Datei(en) gelöscht` })
      };
    }

    // === POST: Neuer Upload (von der Familie) ===
    if (event.httpMethod !== "POST") {
      return { statusCode: 405, headers, body: JSON.stringify({ error: "Nur GET, POST, DELETE" }) };
    }

    const body = JSON.parse(event.body);
    const files = body.files || [];

    if (!files.length) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: "Keine Dateien" }) };
    }

    const uploader = body.uploader || "Familie";
    const description = body.description || "";
    const results = [];

    for (const f of files) {
      if (!f.data) {
        results.push({ filename: f.name, status: "error", error: "Keine Daten" });
        continue;
      }

      const raw = Buffer.from(f.data, "base64");
      if (raw.length > MAX_SIZE) {
        results.push({ filename: f.name, status: "error", error: "Zu groß (max 25 MB)" });
        continue;
      }

      const ext = f.name.split(".").pop()?.toLowerCase();
      if (!ALLOWED.includes(ext)) {
        results.push({ filename: f.name, status: "error", error: `.${ext} nicht erlaubt` });
        continue;
      }

      const { type, icon } = classify(f.name);
      const key = `${Date.now()}-${f.name.replace(/[^a-zA-Z0-9._-]/g, "_")}`;

      try {
        await store.set(key, f.data, {
          metadata: {
            filename: f.name,
            type,
            icon,
            size: raw.length,
            uploader,
            description,
            uploadedAt: new Date().toISOString()
          }
        });

        results.push({ filename: f.name, status: "success", type, icon });
      } catch (err) {
        results.push({ filename: f.name, status: "error", error: err.message });
      }
    }

    const successCount = results.filter(r => r.status === "success").length;
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        message: `${successCount} Datei(en) gespeichert 📸`,
        results,
        hinweis: "LUMI wird die neuen Momente bald verarbeiten 🤖✨"
      })
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message || "Fehler beim Upload" })
    };
  }
};
