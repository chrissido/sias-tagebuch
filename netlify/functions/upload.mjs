// Sias Tagebuch – Upload Function (GitHub Edition)
// Empfängt Uploads, committed sie via GitHub Content API ins Repo
// Netlify auto-deployet nach jedem Commit

import { Buffer } from 'node:buffer';
import { randomUUID } from 'node:crypto';

// === KONFIGURATION ===
// GitHub Token: erst aus Umgebungsvariablen, dann Fallback (für erste Tests)
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || 'ghp_t0...rpmp';
const GITHUB_OWNER = 'chrissido';
const GITHUB_REPO = 'sias-tagebuch';
const BRANCH = 'master';

// Netlify Token: für Deploy-Trigger nach Upload
const NETLIFY_AUTH = process.env.NETLIFY_ACCESS_TOKEN || process.env.NETLIFY_AUTH_TOKEN || 'nfp_...0e';
const NETLIFY_SITE_ID = process.env.SITE_ID || process.env.NETLIFY_SITE_ID || '2818d7ea-91ff-472f-a7ed-fd4cd7298934';

const ALLOWED = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mov', 'webm', 'mp3', 'ogg', 'wav', 'm4a', 'heic', 'heif'];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

// === HELPERS ===

function classify(name) {
  const ext = name.split('.').pop()?.toLowerCase();
  if (['jpg','jpeg','png','gif','webp','heic','heif'].includes(ext)) return { type: 'Bild', icon: '📸' };
  if (['mp4','mov','webm'].includes(ext)) return { type: 'Video', icon: '🎬' };
  if (['mp3','ogg','wav','m4a'].includes(ext)) return { type: 'Audio', icon: '🎤' };
  return { type: 'Datei', icon: '📄' };
}

function formatDate(isoStr) {
  const d = new Date(isoStr);
  return `${String(d.getDate()).padStart(2, '0')}. ${String(d.getMonth() + 1).padStart(2, '0')}. ${d.getFullYear()}`;
}

function sanitizeFilename(name, dateStr) {
  const ext = name.split('.').pop()?.toLowerCase() || 'jpg';
  const datePart = dateStr.split('T')[0] || new Date().toISOString().split('T')[0];
  return `sia-${datePart}-${randomUUID().slice(0, 8)}.${ext}`;
}

// GitHub Content API: File lesen
async function readGitHubFile(path) {
  const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${path}?ref=${BRANCH}`;
  const res = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'lumi-sias-tagebuch',
    },
  });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`GitHub GET ${path}: ${res.status}`);
  const data = await res.json();
  return {
    sha: data.sha,
    content: Buffer.from(data.content, 'base64').toString('utf-8'),
  };
}

// GitHub Content API: File schreiben/updaten
async function writeGitHubFile(path, content, message) {
  const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${path}`;
  const body = {
    message,
    content: Buffer.from(content, 'utf-8').toString('base64'),
    branch: BRANCH,
  };

  // SHA nur bei Update (nicht bei neuen Dateien)
  const existing = await readGitHubFile(path);
  if (existing) body.sha = existing.sha;

  const res = await fetch(url, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${GITHUB_TOKEN}`,
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'lumi-sias-tagebuch',
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`GitHub PUT ${path}: ${res.status} – ${err.slice(0, 200)}`);
  }
  return await res.json();
}

// GitHub Content API: Base64-Datei hochladen (Bild/Video/Audio)
async function uploadBinaryFile(path, base64Data, message) {
  const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${path}`;
  const body = {
    message,
    content: base64Data,
    branch: BRANCH,
  };

  const existing = await readGitHubFile(path);
  if (existing) body.sha = existing.sha;

  const res = await fetch(url, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${GITHUB_TOKEN}`,
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'lumi-sias-tagebuch',
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`GitHub PUT binary ${path}: ${res.status} – ${err.slice(0, 200)}`);
  }
  return await res.json();
}

// Netlify Deploy auslösen (nach GitHub Commit)
async function triggerNetlifyDeploy() {
  const url = `https://api.netlify.com/api/v1/sites/${NETLIFY_SITE_ID}/deploys`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${NETLIFY_AUTH}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
  });
  if (!res.ok) {
    const err = await res.text();
    console.log(`Netlify Deploy trigger: ${res.status} – ${err.slice(0, 100)}`);
    return false;
  }
  return true;
}

// === HANDLER ===

export const handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') return { statusCode: 204, headers, body: '' };

  // GET: Status abfragen
  if (event.httpMethod === 'GET') {
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        mode: 'github',
        message: '✅ GitHub-gestützter Upload – Dateien landen direkt im Repo und werden automatisch deployed',
        repo: `${GITHUB_OWNER}/${GITHUB_REPO}`,
        supported: ALLOWED.map(e => '.' + e).join(', '),
      }),
    };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Nur POST' }) };
  }

  try {
    const body = JSON.parse(event.body);
    const files = body.files || [];
    if (!files.length) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: 'Keine Dateien' }) };
    }

    const uploader = body.uploader || 'Familie';
    const description = body.description || '';
    const now = new Date().toISOString();
    const dateStr = formatDate(now);
    const results = [];

    for (const f of files) {
      if (!f.data) {
        results.push({ filename: f.name, status: 'error', error: 'Keine Daten' });
        continue;
      }

      const raw = Buffer.from(f.data, 'base64');
      if (raw.length > MAX_FILE_SIZE) {
        results.push({ filename: f.name, status: 'error', error: 'Zu groß (max 10 MB)' });
        continue;
      }

      const ext = f.name.split('.').pop()?.toLowerCase();
      if (!ALLOWED.includes(ext)) {
        results.push({ filename: f.name, status: 'error', error: `.${ext} nicht erlaubt` });
        continue;
      }

      const { type, icon } = classify(f.name);
      const safeName = sanitizeFilename(f.name, now);
      const imgPath = `assets/images/${safeName}`;
      const descriptionText = description || `${type} von ${uploader}`;

      try {
        // 1. Bild ins Repo hochladen
        await uploadBinaryFile(imgPath, f.data, `📸 Neues ${type}: ${descriptionText}`);

        // 2. Galerie-Eintrag erstellen
        const galleryEntry = `
        <div class="gallery-item fade-in">
          <img src="${imgPath}" alt="${descriptionText}" class="gallery-item-image" loading="lazy">
          <div class="gallery-item-overlay">
            <div class="gallery-item-title">${descriptionText}</div>
            <div class="gallery-item-date">${dateStr} · von ${uploader}</div>
          </div>
        </div>`;

        // 3. galerie.html aktualisieren
        const galerie = await readGitHubFile('galerie.html');
        if (galerie) {
          let newGalerie = galerie.content;

          // Empty-State ausblenden, Gallery-Grid einblenden
          newGalerie = newGalerie.replace(
            '<div class="empty-state" id="gallery-empty">',
            '<div class="empty-state" id="gallery-empty" style="display: none;">'
          );
          newGalerie = newGalerie.replace(
            '<div class="gallery-grid" id="gallery-grid" style="display: none;">',
            '<div class="gallery-grid" id="gallery-grid">'
          );

          // Neuen Eintrag vor dem schließenden </div> von gallery-grid einfügen
          newGalerie = newGalerie.replace(
            '<!-- Galerie-Einträge werden später von LUMI eingefügt -->',
            `<!-- Galerie-Einträge werden später von LUMI eingefügt -->\n${galleryEntry}`
          );

          await writeGitHubFile('galerie.html', newGalerie, `🖼️ Galerie aktualisiert: ${descriptionText}`);
        }

        // 4. index.html aktualisieren (Neuester Moment)
        const indexPage = await readGitHubFile('index.html');
        if (indexPage) {
          let newIndex = indexPage.content;

          // Latest-Badge aktualisieren
          newIndex = newIndex.replace(
            '<span class="latest-badge">✦ Neuester Eintrag</span>',
            `<span class="latest-badge">✦ Neuester Eintrag</span>`
          );
          newIndex = newIndex.replace(
            '<span class="latest-date">Noch kein Eintrag</span>',
            `<span class="latest-date">${dateStr}</span>`
          );

          // Latest-Moment-Content ersetzen
          const latestContent = `
            <div class="latest-moment-image">
              <img src="${imgPath}" alt="${descriptionText}" style="width: 100%; height: 280px; object-fit: cover; border-radius: 12px;">
            </div>
            <div class="latest-text">
              <p style="font-size: 1.1rem; line-height: 1.6;">${descriptionText}</p>
              <p style="font-size: 0.85rem; color: var(--text-light); margin-top: 0.5rem;">📸 von ${uploader} · ${dateStr}</p>
              <a href="galerie.html" class="btn btn-outline" style="margin-top: 0.8rem;">Alle Momente ansehen</a>
            </div>`;

          // Alten Content ersetzen (zwischen latest-moment-content)
          newIndex = newIndex.replace(
            /<div class="latest-moment-content">[\s\S]*?<\/div>\s*<\/div>\s*<\/section>/,
            `<div class="latest-moment-content">${latestContent}</div></div></section>`
          );

          // Statistik aktualisieren (Momente-Zähler erhöhen)
          // Einfach den aktuellen Wert durch ein Update ersetzen – den genauen Zähler kennen wir nicht
          // Also ersetzen wir stattdessen die ganze stat-card für Momente
          // Wird später verfeinert

          await writeGitHubFile('index.html', newIndex, `🏠 Startseite aktualisiert: ${descriptionText}`);
        }

        results.push({
          filename: f.name,
          savedAs: safeName,
          status: 'success',
          type,
          icon,
          size: raw.length,
          uploader,
          description: descriptionText,
          date: dateStr,
        });

      } catch (err) {
        results.push({
          filename: f.name,
          status: 'error',
          error: err.message || 'GitHub API Fehler',
        });
      }
    }

    // 5. Netlify Deploy auslösen
    const successCount = results.filter(r => r.status === 'success').length;
    if (successCount > 0) {
      try {
        await triggerNetlifyDeploy();
      } catch (deployErr) {
        // Nicht kritisch – GitHub Push hat trotzdem stattgefunden
        console.log('Deploy trigger fehlgeschlagen:', deployErr.message);
      }
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        message: `${successCount} von ${files.length} Datei(en) erfolgreich ins Tagebuch eingefügt 🎉`,
        results,
        note: 'Die Seite wird in 1-2 Minuten aktualisiert – GitHub + Netlify arbeiten im Hintergrund 🤖✨',
      }),
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message || 'Fehler' }),
    };
  }
};
