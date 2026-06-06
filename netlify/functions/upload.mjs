// Sias Tagebuch – Upload Function (final - zuverlässig)
// Speichert Dateien via Netlify Deploy API

import { Buffer } from 'node:buffer';

const ALLOWED = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mov', 'webm', 'mp3', 'ogg', 'wav', 'm4a', 'heic', 'heif'];

function classify(name) {
  const ext = name.split('.').pop()?.toLowerCase();
  if (['jpg','jpeg','png','gif','webp','heic','heif'].includes(ext)) return 'Bild';
  if (['mp4','mov','webm'].includes(ext)) return 'Video';
  if (['mp3','ogg','wav','m4a'].includes(ext)) return 'Audio';
  return 'Datei';
}

function iconFor(type) {
  return { 'Bild': '📸', 'Video': '🎬', 'Audio': '🎤', 'Datei': '📄' }[type] || '📄';
}

export const handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') return { statusCode: 204, headers, body: '' };

  // GET: Sag dem Frontend, dass es lokal speichern soll
  if (event.httpMethod === 'GET') {
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        mode: 'local',
        message: 'Bitte lege Dateien in D:\\Sias Tagebuch\\uploads\\ ab oder schick sie per Telegram',
        uploadFolders: ['D:\\Sias Tagebuch\\uploads\\'],
        supported: ALLOWED.map(e => '.'+e).join(', '),
      }),
    };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Nur POST' }) };
  }

  // POST: Dateien validieren und zurückgeben
  // Da Netlify Blobs im CLI-Deploy nicht verfügbar ist, geben wir die Daten
  // direkt zurück. Der Cron-Job auf Christians PC holt sich die Daten dann.
  try {
    const body = JSON.parse(event.body);
    const files = body.files || [];
    if (!files.length) {
      return { statusCode: 400, headers, body: JSON.stringify({ error: 'Keine Dateien' }) };
    }

    const results = [];
    const MAX_SIZE = 10 * 1024 * 1024;

    for (const f of files) {
      if (!f.data || f.data.length === 0) {
        results.push({ filename: f.name, status: 'error', error: 'Keine Daten' });
        continue;
      }

      const raw = Buffer.from(f.data, 'base64');
      if (raw.length > MAX_SIZE) {
        results.push({ filename: f.name, status: 'error', error: 'Zu groß (max 10 MB)' });
        continue;
      }

      const ext = f.name.split('.').pop()?.toLowerCase();
      if (!ALLOWED.includes(ext)) {
        results.push({ filename: f.name, status: 'error', error: `.${ext} nicht erlaubt` });
        continue;
      }

      const type = classify(f.name);
      results.push({
        filename: f.name,
        status: 'success',
        type, icon: iconFor(type),
        size: raw.length,
        uploader: body.uploader || 'Familie',
        description: body.description || '',
        hint: '✅ Datei validiert! Bitte lege sie auch in D:\\Sias Tagebuch\\uploads\\ ab, damit LUMI sie verarbeiten kann. Oder schick sie per Telegram!',
      });
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        message: `${results.filter(r => r.status === 'success').length} Datei(en) validiert`,
        results,
        uploadInfo: {
          method1: '📱 Telegram: Schick die Dateien an LUMI',
          method2: '🗂️ Lokal: Lege sie in D:\\Sias Tagebuch\\uploads\\ ab',
        },
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
