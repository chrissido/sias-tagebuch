/** ==========================================
 *  GALLERY – Sias Tagebuch
 *  Monats-Ordner, nach Datum sortiert
 *  ========================================== */

document.addEventListener('DOMContentLoaded', async () => {
  const container = document.getElementById('gallery-container');
  const empty = document.getElementById('gallery-empty');
  if (!container) return;

  let aktuellerFilter = 'all';
  let alleMomente = [];

  try {
    const res = await fetch('momente.json');
    alleMomente = await res.json();

    // Neueste zuerst
    alleMomente.sort((a, b) => new Date(b.datum) - new Date(a.datum));

    renderGalerie('neue');

    // Tabs / Kategorie-Auswahl
    document.querySelectorAll('.gallery-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.gallery-tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        aktuellerFilter = btn.dataset.filter;
        renderGalerie(aktuellerFilter);
      });
    });

  } catch (err) {
    container.innerHTML = '';
    empty.style.display = 'block';
    console.error('Galerie Fehler:', err);
  }

  function renderGalerie(filter) {
    container.innerHTML = '';

    let gefiltert;
    if (filter === 'neue') {
      // Die 20 neuesten Einträge (nach ID, absteigend)
      gefiltert = alleMomente
        .filter(m => m.bild)
        .sort((a, b) => b.id - a.id)
        .slice(0, 20);
    } else if (filter === 'all') {
      gefiltert = alleMomente;
    } else {
      gefiltert = alleMomente.filter(m => m.typ === filter);
    }

    if (gefiltert.length === 0) {
      container.style.display = 'none';
      empty.style.display = 'block';
      return;
    }

    container.style.display = 'block';
    empty.style.display = 'none';

    // Nach Monat gruppieren
    const monate = {};
    gefiltert.forEach(m => {
      const d = new Date(m.datum);
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
      const label = d.toLocaleDateString('de-DE', { month: 'long', year: 'numeric' });
      if (!monate[key]) monate[key] = { label, eintraege: [] };
      monate[key].eintraege.push(m);
    });

    // Monate sortieren (neueste zuerst)
    const sortierteMonate = Object.entries(monate).sort((a, b) => b[0].localeCompare(a[0]));

    sortierteMonate.forEach(([key, monat]) => {
      // Monats-Sektion
      const section = document.createElement('div');
      section.className = 'gallery-month fade-in';

      const header = document.createElement('div');
      header.className = 'gallery-month-header';
      header.innerHTML = `
        <h2 class="gallery-month-title">${monat.label}</h2>
        <span class="gallery-month-count">${monat.eintraege.length} ${monat.eintraege.length === 1 ? 'Eintrag' : 'Einträge'}</span>
      `;
      section.appendChild(header);

      // Grid
      const grid = document.createElement('div');
      grid.className = 'gallery-grid';

      monat.eintraege.forEach((m, i) => {
        const card = document.createElement('div');
        card.className = `gallery-card fade-in${m.bild ? '' : ' no-image'}`;
        card.style.animationDelay = `${i * 0.06}s`;

        if (m.bild) {
          const img = document.createElement('img');
          img.src = m.bild;
          img.alt = m.titel;
          img.loading = 'lazy';
          card.appendChild(img);

          card.onclick = () => openLightbox(m.bild);

          const overlay = document.createElement('div');
          overlay.className = 'gallery-card-overlay';
          overlay.innerHTML = `
            <div class="gallery-card-title">${m.titel}</div>
            <div class="gallery-card-date">${formatDatumKurz(new Date(m.datum))}</div>
          `;
          card.appendChild(overlay);

        } else {
          // Meilenstein ohne Bild
          const icon = document.createElement('div');
          icon.className = 'gallery-card-icon';
          icon.textContent = '👣';
          card.appendChild(icon);

          const title = document.createElement('div');
          title.className = 'gallery-card-title';
          title.textContent = m.titel;
          card.appendChild(title);

          const date = document.createElement('div');
          date.className = 'gallery-card-date';
          date.textContent = formatDatumLang(new Date(m.datum));
          card.appendChild(date);
        }

        grid.appendChild(card);
      });

      section.appendChild(grid);
      container.appendChild(section);
    });
  }
});

/** Lightbox öffnen */
function openLightbox(src) {
  const existing = document.querySelector('.lightbox');
  if (existing) existing.remove();

  const lb = document.createElement('div');
  lb.className = 'lightbox active';
  lb.onclick = (e) => { if (e.target === lb) lb.remove(); };

  const img = document.createElement('img');
  img.src = src;
  lb.appendChild(img);

  const close = document.createElement('button');
  close.className = 'lightbox-close';
  close.innerHTML = '✕';
  close.onclick = () => lb.remove();
  lb.appendChild(close);

  document.body.appendChild(lb);

  const escHandler = (e) => {
    if (e.key === 'Escape') { lb.remove(); document.removeEventListener('keydown', escHandler); }
  };
  document.addEventListener('keydown', escHandler);
}

/** Datum formatieren */
function formatDatumLang(date) {
  return date.toLocaleDateString('de-DE', {
    day: 'numeric', month: 'long', year: 'numeric'
  });
}

function formatDatumKurz(date) {
  return date.toLocaleDateString('de-DE', {
    day: '2-digit', month: '2-digit', year: 'numeric'
  });
}
