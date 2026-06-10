/**
 *  UPLOAD – Sias Tagebuch
 *  Version 2: Vorschau + Beschreibung pro Foto + iOS-sicher
 *  ========================================== */

document.addEventListener('DOMContentLoaded', () => {

  // ─── DOM-Referenzen ───
  const dropzone = document.getElementById('dropzone');
  const selectBtn = document.getElementById('select-btn');
  const addMoreBtn = document.getElementById('add-more-btn');
  const previewGrid = document.getElementById('preview-grid');
  const submitBtn = document.getElementById('upload-submit');
  const nameInput = document.getElementById('uploader-name');
  const stepSelect = document.getElementById('step-select');
  const stepPreview = document.getElementById('step-preview');
  const stepStatus = document.getElementById('step-status');
  const statusEl = document.getElementById('upload-status');
  const resetBtn = document.getElementById('reset-btn');

  // ─── iOS-sicherer File-Input ───
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.multiple = true;
  fileInput.accept = 'image/jpeg,image/png,image/webp,image/heic,image/heif,video/mp4,video/quicktime';
  // opacity 0.01 + absolute Position (nicht hidden/display:none – das blockiert iOS!)
  fileInput.style.cssText = 'position:fixed;top:-100px;left:-100px;width:1px;height:1px;opacity:0.01;z-index:-1;';
  document.body.appendChild(fileInput);

  let selectedFiles = []; // {file, description, thumbUrl}

  // ─── Dateien auswählen (Button → fileInput.click()) ───
  function openFilePicker() {
    fileInput.value = ''; // reset, damit change-Event auch bei gleicher Auswahl feuert
    fileInput.click();
  }

  selectBtn.addEventListener('click', (e) => {
    e.preventDefault();
    openFilePicker();
  });

  addMoreBtn.addEventListener('click', (e) => {
    e.preventDefault();
    openFilePicker();
  });

  // ─── Thumbnail erstellen (Bild) ───
  function createThumbnail(file) {
    return new Promise((resolve) => {
      if (file.type.startsWith('video/')) {
        // Video: erstes Frame als Thumbnail
        const video = document.createElement('video');
        video.preload = 'metadata';
        video.muted = true;
        video.playsInline = true;
        const url = URL.createObjectURL(file);
        video.src = url;
        video.onloadeddata = () => {
          video.currentTime = 0.5;
        };
        video.onseeked = () => {
          const canvas = document.createElement('canvas');
          canvas.width = 160;
          canvas.height = 120;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(video, 0, 0, 160, 120);
          resolve(canvas.toDataURL('image/jpeg', 0.7));
          URL.revokeObjectURL(url);
        };
        video.onerror = () => {
          resolve(null);
          URL.revokeObjectURL(url);
        };
      } else {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.readAsDataURL(file);
      }
    });
  }

  // ─── Vorschau-Karte für ein Foto erstellen ───
  function createPreviewCard(file, description) {
    const card = document.createElement('div');
    card.className = 'preview-card';
    card.dataset.index = selectedFiles.length;

    const sizeStr = (file.size / 1024 / 1024).toFixed(1) + ' MB';
    const thumbUrl = description || '';

    card.innerHTML = `
      <div class="preview-thumb">
        <img src="${thumbUrl || ''}" alt="${file.name}" onerror="this.style.display='none'">
        <span class="preview-type">${file.type.startsWith('video/') ? '🎬' : '📷'}</span>
      </div>
      <div class="preview-body">
        <div class="preview-header">
          <span class="preview-filename">${file.name}</span>
          <span class="preview-size">${sizeStr}</span>
          <button class="preview-remove" title="Entfernen">&times;</button>
        </div>
        <textarea class="preview-desc" rows="3" placeholder="Was ist auf dem Foto zu sehen? z.B. Sia spielt im Garten mit den Gänseblümchen…">${selectedFiles.length > 0 && selectedFiles[selectedFiles.length-1] && selectedFiles[selectedFiles.length-1].description || ''}</textarea>
      </div>
    `;

    // Entfernen-Button
    const removeBtn = card.querySelector('.preview-remove');
    removeBtn.addEventListener('click', () => {
      const idx = parseInt(card.dataset.index);
      selectedFiles.splice(idx, 1);
      renderPreviewCards();
    });

    // Description-Änderungen speichern
    const descField = card.querySelector('.preview-desc');
    descField.addEventListener('input', () => {
      const idx = parseInt(card.dataset.index);
      if (idx >= 0 && idx < selectedFiles.length) {
        selectedFiles[idx].description = descField.value;
      }
    });

    return card;
  }

  // ─── Vorschau-Karten rendern ───
  function renderPreviewCards() {
    previewGrid.innerHTML = '';
    selectedFiles.forEach((item, idx) => {
      const card = createPreviewCard(item.file, item.thumbUrl);
      card.dataset.index = idx;
      const descField = card.querySelector('.preview-desc');
      descField.value = item.description || '';
      previewGrid.appendChild(card);
    });
    submitBtn.disabled = selectedFiles.length === 0;
    submitBtn.textContent = selectedFiles.length > 0
      ? `Alle ${selectedFiles.length} Fotos hochladen`
      : 'Alle hochladen';
  }

  // ─── Dateien verarbeiten ───
  async function handleFiles(files) {
    const fileArray = Array.from(files);
    let addedCount = 0;

    for (const file of fileArray) {
      if (file.size > 10 * 1024 * 1024) {
        alert(`"${file.name}" ist zu groß (max 10 MB)`);
        continue;
      }
      const thumbUrl = await createThumbnail(file);
      selectedFiles.push({
        file: file,
        description: '',
        thumbUrl: thumbUrl,
      });
      addedCount++;
    }

    if (addedCount === 0) return;

    // Zu Schritt 2 wechseln
    stepSelect.style.display = 'none';
    stepStatus.style.display = 'none';
    stepPreview.style.display = 'block';

    renderPreviewCards();
  }

  // ─── File-Input Change-Event ───
  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length) {
      handleFiles(e.target.files);
    }
  });

  // ─── Drag & Drop ───
  let dragCounter = 0;

  dropzone.addEventListener('dragenter', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter++;
    dropzone.classList.add('dragover');
  });

  dropzone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter--;
    if (dragCounter <= 0) {
      dragCounter = 0;
      dropzone.classList.remove('dragover');
    }
  });

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter = 0;
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      handleFiles(e.dataTransfer.files);
    }
  });

  // ─── Hochladen ───
  submitBtn.addEventListener('click', async () => {
    if (!selectedFiles.length) return;

    submitBtn.disabled = true;
    submitBtn.textContent = 'Wird hochgeladen …';

    // Letzte Beschreibungen aus DOM holen
    const cards = previewGrid.querySelectorAll('.preview-card');
    cards.forEach((card) => {
      const idx = parseInt(card.dataset.index);
      const desc = card.querySelector('.preview-desc').value;
      if (idx >= 0 && idx < selectedFiles.length) {
        selectedFiles[idx].description = desc;
      }
    });

    let successCount = 0;
    let errorCount = 0;
    const total = selectedFiles.length;

    // Status-Ansicht vorbereiten
    stepPreview.style.display = 'none';
    stepStatus.style.display = 'block';
    statusEl.className = 'upload-status sending';
    statusEl.innerHTML = `<p>📤 0 / ${total} hochgeladen …</p>`;

    // Jede Datei einzeln hochladen
    for (let i = 0; i < selectedFiles.length; i++) {
      const item = selectedFiles[i];
      const file = item.file;

      try {
        statusEl.innerHTML = `<p>📤 ${i + 1} / ${total} – ${file.name} …</p>`;

        // Datei als Base64
        const base64 = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(reader.result.split(',')[1]);
          reader.onerror = () => reject(new Error('Konnte Datei nicht lesen'));
          reader.readAsDataURL(file);
        });

        const res = await fetch('/upload', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            files: [{
              name: file.name,
              mimeType: file.type || 'image/jpeg',
              data: base64,
              description: item.description || '',
            }],
            uploader: nameInput.value.trim() || 'Familie',
          }),
        });

        const data = await res.json();

        if (res.ok && data.results && data.results[0]?.status === 'success') {
          successCount++;
        } else {
          throw new Error(data.results?.[0]?.error || 'Fehler');
        }

      } catch (err) {
        errorCount++;
      }
    }

    // Ergebnis
    if (errorCount === 0) {
      statusEl.className = 'upload-status success';
      statusEl.innerHTML = `
        <p style="font-size:1.6rem;margin:0 0 0.3rem;">🎉</p>
        <p><strong>Alle ${successCount} Fotos erfolgreich hochgeladen!</strong></p>
        <p style="font-size:0.85rem;color:var(--text-muted);">LUMI verarbeitet sie beim nächsten Durchlauf.</p>
      `;
    } else {
      statusEl.className = 'upload-status error';
      statusEl.innerHTML = `
        <p>⚠️ ${successCount} von ${total} erfolgreich hochgeladen</p>
        <p style="font-size:0.85rem;color:var(--text-muted);">${errorCount} Fehler – bitte versuche es erneut.</p>
      `;
    }
  });

  // ─── Reset ───
  resetBtn.addEventListener('click', () => {
    selectedFiles = [];
    previewGrid.innerHTML = '';
    stepStatus.style.display = 'none';
    stepSelect.style.display = 'block';
    stepPreview.style.display = 'none';
    submitBtn.disabled = true;
    submitBtn.textContent = 'Alle hochladen';
    nameInput.value = '';
  });

  // ─── Nav-Toggle (falls nicht in main.js) ───
  const navToggle = document.querySelector('.nav-toggle');
  if (navToggle) {
    navToggle.addEventListener('click', () => {
      const expanded = navToggle.getAttribute('aria-expanded') === 'true' ? false : true;
      navToggle.setAttribute('aria-expanded', expanded);
      document.querySelector('.nav-links').classList.toggle('open');
    });
  }

});
