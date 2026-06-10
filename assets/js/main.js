/* ============================================
   Sias Tagebuch – Interaktivität
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ---------- Auto-Hide Nav beim Scrollen ----------
  let lastScroll = 0;
  const nav = document.querySelector('nav');
  const SCROLL_THRESHOLD = 10;

  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;

    if (currentScroll <= 0) {
      // Ganz oben → immer zeigen
      nav.classList.remove('nav-hidden');
    } else if (currentScroll > lastScroll + SCROLL_THRESHOLD) {
      // Runter scrollen → verstecken
      nav.classList.add('nav-hidden');
    } else if (currentScroll < lastScroll - SCROLL_THRESHOLD) {
      // Hoch scrollen → zeigen
      nav.classList.remove('nav-hidden');
    }

    lastScroll = currentScroll;
  });

  // ---------- Hamburger Menü ----------
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  
  if (toggle) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      // ARIA support
      const expanded = navLinks.classList.contains('open');
      toggle.setAttribute('aria-expanded', expanded);
    });

    // Menü schließen bei Klick auf Link
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });

    // Menü schließen bei Klick außerhalb
    document.addEventListener('click', (e) => {
      if (!e.target.closest('nav') && navLinks.classList.contains('open')) {
        navLinks.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ---------- Aktive Nav-Seite markieren ----------
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath) {
      link.classList.add('active');
    }
  });

  // ---------- Aktuelles Alter berechnen ----------
  const ageElements = document.querySelectorAll('[data-age]');
  if (ageElements.length > 0) {
    const birthDate = new Date(2025, 0, 7); // 07. Januar 2025
    const today = new Date();
    
    let years = today.getFullYear() - birthDate.getFullYear();
    let months = today.getMonth() - birthDate.getMonth();
    let days = today.getDate() - birthDate.getDate();
    
    if (days < 0) {
      months--;
      const prevMonth = new Date(today.getFullYear(), today.getMonth(), 0);
      days += prevMonth.getDate();
    }
    
    if (months < 0) {
      years--;
      months += 12;
    }
    
    let ageText = '';
    if (years > 0) {
      ageText = `${years} Jahr${years > 1 ? 'e' : ''}`;
      if (months > 0) ageText += ` und ${months} Monat${months > 1 ? 'e' : ''}`;
    } else {
      ageText = `${months} Monat${months > 1 ? 'e' : ''}`;
      if (days > 0) ageText += ` (${days} Tage)`;
    }
    
    ageElements.forEach(el => {
      el.textContent = ageText;
    });
  }

  // ---------- Sanftes Einblenden beim Scrollen ----------
  const fadeElements = document.querySelectorAll('.fade-in');
  
  if (fadeElements.length > 0 && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });
    
    fadeElements.forEach(el => observer.observe(el));
  }

  // ---------- Zufällige bunte Platzhalter-Farben für die Galerie ----------
  const placeholderColors = [
    'linear-gradient(135deg, #B8D4C7, #D4E8DE)',
    'linear-gradient(135deg, #E8C4B8, #F2D9D0)',
    'linear-gradient(135deg, #D4B896, #E8D4BC)',
    'linear-gradient(135deg, #B8C9A8, #D4DFC4)',
    'linear-gradient(135deg, #C4B8D4, #DED0E8)',
    'linear-gradient(135deg, #B8D4D4, #D0E8E8)'
  ];

  document.querySelectorAll('.gallery-item-empty').forEach((el, i) => {
    el.style.background = placeholderColors[i % placeholderColors.length];
  });

  // ---------- Lade Bild: wenn vorhanden, korrekt anzeigen ----------
  // Alle gallery-item-image: falls src fehlt oder fehlerhaft, Platzhalter zeigen
  document.querySelectorAll('.gallery-item-image').forEach(img => {
    img.addEventListener('error', function() {
      this.style.display = 'none';
      const parent = this.closest('.gallery-item');
      if (parent) {
        const overlay = parent.querySelector('.gallery-item-overlay');
        if (overlay) overlay.style.opacity = '1';
      }
    });
  });

  // ========== UPLOAD FUNKTIONEN ==========

  // ---------- Drag & Drop ----------
  const dropZone = document.getElementById('drop-zone');
  let dragCounter = 0;

  document.addEventListener('dragenter', (e) => {
    e.preventDefault();
    dragCounter++;
    if (dropZone) dropZone.classList.add('visible');
  });

  document.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dragCounter--;
    if (dragCounter <= 0 && dropZone) {
      dropZone.classList.remove('visible');
      dragCounter = 0;
    }
  });

  document.addEventListener('dragover', (e) => {
    e.preventDefault();
  });

  document.addEventListener('drop', (e) => {
    e.preventDefault();
    if (dropZone) dropZone.classList.remove('visible');
    dragCounter = 0;
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFiles(files);
    }
  });

  // ---------- Klick auf Upload-Methode ----------
  const methodUpload = document.getElementById('method-upload');
  const fileInput = document.getElementById('file-input');

  if (methodUpload && fileInput) {
    methodUpload.addEventListener('click', () => {
      fileInput.click();
    });
  }

  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        handleFiles(e.target.files);
        fileInput.value = '';
      }
    });
  }

  // ---------- Dateien verarbeiten (Upload zu Netlify → GitHub) ----------
  const UPLOAD_URL = '/.netlify/functions/upload';

  function handleFiles(files) {
    const list = document.getElementById('upload-list');
    const empty = document.getElementById('empty-queue');
    const badge = document.getElementById('queue-count');

    if (empty) empty.style.display = 'none';
    if (list) list.innerHTML = '';

    const uploaderName = document.getElementById('uploader-name');
    const uploadDesc = document.getElementById('upload-description');

    // Lade-Status anzeigen
    if (list) {
      list.innerHTML = `
        <div class="upload-item fade-in visible">
          <div class="upload-item-thumb">⏳</div>
          <div class="upload-item-info">
            <div class="upload-item-title">${files.length} Datei(en) werden verarbeitet…</div>
            <div class="upload-item-meta" id="upload-progress">Lese Dateien ein…</div>
          </div>
          <span class="upload-item-status status-processing">lade</span>
        </div>
      `;
    }

    // Dateien in Base64 umwandeln
    const promises = [];
    for (const file of files) {
      promises.push(new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          const base64 = reader.result.split(',')[1];
          resolve({ name: file.name, mimeType: file.type, data: base64 });
        };
        reader.onerror = () => reject(new Error(`Fehler beim Lesen von ${file.name}`));
        reader.readAsDataURL(file);
      }));
    }

    const progress = document.getElementById('upload-progress');

    Promise.all(promises)
      .then(fileData => {
        if (progress) progress.textContent = 'Sende an LUMI…';
        return fetch(UPLOAD_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            files: fileData,
            uploader: uploaderName ? uploaderName.value : 'Familie',
            description: uploadDesc ? uploadDesc.value : '',
          }),
        });
      })
      .then(res => res.json())
      .then(data => {
        if (data.error) throw new Error(data.error);

        if (list) list.innerHTML = '';
        let successCount = 0;

        data.results.forEach(item => {
          if (item.status === 'success') successCount++;
          const div = document.createElement('div');
          div.className = 'upload-item fade-in';
          div.innerHTML = `
            <div class="upload-item-thumb">${item.icon || '📄'}</div>
            <div class="upload-item-info">
              <div class="upload-item-title">${item.filename}</div>
              <div class="upload-item-meta">${item.type || 'Datei'} · gespeichert ✅</div>
            </div>
            <span class="upload-item-status ${item.status === 'success' ? 'status-done' : 'status-new'}">
              ${item.status === 'success' ? '✅ gespeichert' : '❌ ' + (item.error || 'Fehler')}
            </span>
          `;
          if (list) list.appendChild(div);
        });

        if (badge) badge.textContent = `${successCount} neu`;

        if (successCount > 0) {
          const note = document.createElement('div');
          note.className = 'upload-item fade-in visible';
          note.style.borderTop = '1px solid rgba(154, 140, 120, 0.1)';
          note.style.paddingTop = '1rem';
          note.style.marginTop = '0.5rem';
          note.innerHTML = `
            <div class="upload-item-info" style="text-align: center;">
              <div class="upload-item-title" style="color: var(--sage-dark);">✨ ${successCount} Datei(en) gespeichert!</div>
              <div class="upload-item-meta">LUMI wird die neuen Momente gleich verarbeiten 🤖✨</div>
            </div>
          `;
          if (list) list.appendChild(note);
        }

        setTimeout(() => {
          document.querySelectorAll('#upload-list .fade-in').forEach(el => el.classList.add('visible'));
        }, 100);
      })
      .catch(err => {
        if (list) {
          list.innerHTML = `
            <div class="upload-item fade-in visible">
              <div class="upload-item-thumb">⚠️</div>
              <div class="upload-item-info">
                <div class="upload-item-title">Upload fehlgeschlagen</div>
                <div class="upload-item-meta">Bitte versuch es später nochmal 📱</div>
              </div>
              <span class="upload-item-status status-new">Fehler</span>
            </div>
          `;
        }
      });
  }

  // ---------- Methode: Telegram (Info) ----------
  const methodTelegram = document.getElementById('method-telegram');
  if (methodTelegram) {
    methodTelegram.addEventListener('click', () => {
      methodTelegram.classList.toggle('active');
      if (methodTelegram.classList.contains('active')) {
        const list = document.getElementById('upload-list');
        const empty = document.getElementById('empty-queue');
        if (empty) empty.style.display = 'none';
        if (list) {
          list.innerHTML = `
            <div class="upload-item fade-in visible">
              <div class="upload-item-thumb">📱</div>
              <div class="upload-item-info">
                <div class="upload-item-title">Telegram ist verbunden ✅</div>
                <div class="upload-item-meta">Schick mir Medien – ich leite sie ans Tagebuch weiter</div>
              </div>
              <span class="upload-item-status status-processing">aktiv</span>
            </div>
          `;
        }
      }
    });
  }

  // ---------- Methode: Ordner ----------
  const methodFolder = document.getElementById('method-folder');
  if (methodFolder) {
    methodFolder.addEventListener('click', () => {
      methodFolder.classList.toggle('active');
      if (methodFolder.classList.contains('active')) {
        const list = document.getElementById('upload-list');
        const empty = document.getElementById('empty-queue');
        if (empty) empty.style.display = 'none';
        if (list) {
          list.innerHTML = `
            <div class="upload-item fade-in visible">
              <div class="upload-item-thumb">🗂️</div>
              <div class="upload-item-info">
                <div class="upload-item-title">Upload-Ordner</div>
                <div class="upload-item-meta">Dateien in D:\\Sias Tagebuch\\uploads\\ ablegen – LUMI findet sie 📂</div>
              </div>
              <span class="upload-item-status status-new">bereit</span>
            </div>
          `;
        }
      }
    });
  }

});
