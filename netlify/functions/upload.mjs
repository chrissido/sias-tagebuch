// upload.mjs – LUMI Upload Proxy
// Nimmt Dateien von der Website entgegen und leitet sie
// an den Cloudflare Tunnel → lumi-server.py auf Christians PC weiter.
// 🚇 Tunnel-URL – diese URL ändert sich bei jedem Tunnel-Neustart!
// Wenn der Tunnel neugestartet wird, musst du diese URL aktualisieren
// und neu deployen (git push)!
const TUNNEL_URL = "https://better-sensitive-equation-theorem.trycloudflare.com";
const MAX_SIZE = 10 * 1024 * 1024; // 10 MB (Netlify Free Limit)
const ALLOWED = ["jpg","jpeg","png","gif","webp","mp4","mov","webm","mp3","ogg","wav","m4a","heic","heif"];

const headers = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json"
};

export const handler = async (event) => {
  // CORS Preflight
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers, body: "" };
  }

  // Nur POST
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, headers, body: JSON.stringify({ error: "Nur POST erlaubt" }) };
  }

  // Prüfen ob Tunnel-URL konfiguriert ist
  if (!TUNNEL_URL) {
    return {
      statusCode: 503,
      headers,
      body: JSON.stringify({
        error: "Der LUMI-Server ist gerade nicht erreichbar.",
        hint: "Bitte versuch es später nochmal oder schick die Dateien per Telegram 📱"
      })
    };
  }

  try {
    const body = JSON.parse(event.body);
    const files = body.files || [];

    if (!files.length) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: "Keine Dateien" }) };
    }

    // Dateien validieren
    const validFiles = [];
    const results = [];

    for (const f of files) {
      if (!f.data) {
        results.push({ filename: f.name, status: "error", error: "Keine Daten" });
        continue;
      }

      const raw = Buffer.from(f.data, "base64");
      if (raw.length > MAX_SIZE) {
        results.push({ filename: f.name, status: "error", error: "Zu groß (max 10 MB)" });
        continue;
      }

      const ext = f.name.split(".").pop()?.toLowerCase();
      if (!ALLOWED.includes(ext)) {
        results.push({ filename: f.name, status: "error", error: `.${ext} nicht erlaubt` });
        continue;
      }

      validFiles.push(f);
    }

    // Wenn keine validen Dateien, gleich zurückschicken
    if (validFiles.length === 0) {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ message: "Keine gültigen Dateien", results })
      };
    }

    // An den Tunnel weiterleiten
    const tunnelResponse = await fetch(TUNNEL_URL + "/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        files: validFiles,
        uploader: body.uploader || "Familie",
        description: body.description || ""
      })
    });

    if (!tunnelResponse.ok) {
      const errText = await tunnelResponse.text();
      throw new Error(`Tunnel-Fehler: ${tunnelResponse.status} – ${errText.slice(0, 200)}`);
    }

    const tunnelData = await tunnelResponse.json();

    // Ergebnisse mischen (validierte + Tunnel-Ergebnisse)
    const allResults = [...results, ...(tunnelData.results || [])];
    const successCount = allResults.filter(r => r.status === "success").length;

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        message: `${successCount} Datei(en) gespeichert 📸`,
        results: allResults
      })
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: error.message || "Fehler beim Upload",
        hint: "Bitte versuch es später nochmal oder schick die Dateien per Telegram 📱"
      })
    };
  }
};
