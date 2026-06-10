/** ==========================================
 *  TIMELINE v6 – Sias Tagebuch
 *  Datum mittig, Bilder links/rechts
 *  ========================================== */

document.addEventListener('DOMContentLoaded', async () => {
  const timeline = document.getElementById('timeline');
  if (!timeline) return;

  try {
    const res = await fetch('momente.json');
    let momente = await res.json();
    momente.sort((a, b) => new Date(a.datum) - new Date(b.datum));

    // Nur Timeline-Einträge anzeigen (chronologisch)
    const timelineEintraege = momente.filter(m => m.timeline !== false);

    document.getElementById('stat-eintraege').textContent = `${timelineEintraege.length} Einträge`;
    if (timelineEintraege.length > 0) {
      const eD = new Date(timelineEintraege[0].datum);
      const lD = new Date(timelineEintraege[timelineEintraege.length - 1].datum);
      document.getElementById('stat-zeitraum').textContent = `${fmtKurz(eD)} – ${fmtKurz(lD)}`;
    }

    const groessen = ['normal', 'normal', 'groß', 'normal', 'breit', 'normal', 'hoch', 'normal', 'groß'];
    const pastelFarben = ['mint', 'rose', 'creme', 'lavendel', 'pfirsich', 'hellblau', 'gold'];

    timelineEintraege.forEach((m, i) => {
      const side = i % 2 === 0 ? 'left' : 'right';
      const item = document.createElement('div');
      item.className = `tl-item${m.bild ? ' has-img' : ''}`;
      item.dataset.side = side;
      item.dataset.size = groessen[i % groessen.length];

      // ---- Datum mittig + Linie hat Lücke ----
      const dateWrap = document.createElement('div');
      dateWrap.className = 'tl-date';
      dateWrap.textContent = fmtKurz(new Date(m.datum));
      item.appendChild(dateWrap);

      // ---- Karte ----
      const card = document.createElement('div');
      card.className = `tl-card tl-card--${pastelFarben[i % pastelFarben.length]}`;

      const title = document.createElement('h3');
      title.className = 'tl-title';
      title.textContent = m.titel;
      card.appendChild(title);

      if (m.beschreibung) {
        const p = document.createElement('p');
        p.className = 'tl-text';
        p.textContent = m.beschreibung;
        card.appendChild(p);
      }

      const meta = document.createElement('div');
      meta.className = 'tl-meta';
      let mt = '';
      if (m.autor) mt += `✎ ${m.autor}`;
      if (m.ort) mt += ` · 📍 ${m.ort}`;
      meta.textContent = mt;
      card.appendChild(meta);

      if (m.bild) {
        const imgWrap = document.createElement('div');
        imgWrap.className = 'tl-img';
        const img = document.createElement('img');
        img.src = m.bild;
        img.alt = m.titel;
        img.loading = 'lazy';
        imgWrap.appendChild(img);
        imgWrap.onclick = () => lightbox(m.bild);
        card.appendChild(imgWrap);
      }

      item.appendChild(card);
      timeline.appendChild(item);
    });

    // Alter
    const h = new Date();
    const g = new Date(2025, 0, 7);
    const mm = (h.getFullYear() - g.getFullYear()) * 12 + (h.getMonth() - g.getMonth());
    const j = Math.floor(mm / 12);
    const r = mm % 12;
    let t = '';
    if (j > 0) t += `${j} Jahr${j > 1 ? 'e' : ''} `;
    t += `${r} Monat${r !== 1 ? 'e' : ''}`;
    document.getElementById('end-alter').textContent = t;

    // Scroll-Animation
    const items = document.querySelectorAll('.tl-item');
    const endEl = document.getElementById('timeline-end');
    const allObserve = endEl ? [...items, endEl] : items;
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) entry.target.classList.add('visible');
          else entry.target.classList.remove('visible');
        });
      }, { threshold: 0.2 });
      allObserve.forEach(el => observer.observe(el));
    } else {
      allObserve.forEach(el => el.classList.add('visible'));
    }

  } catch (err) {
    timeline.innerHTML = `<div class="empty-state"><div class="empty-state-icon">📖</div><h3>Noch keine Einträge</h3><p>Hier entsteht Sias Geschichte.</p></div>`;
    console.error(err);
  }
});

function lightbox(src) {
  const old = document.querySelector('.lightbox');
  if (old) old.remove();
  const lb = document.createElement('div');
  lb.className = 'lightbox active';
  lb.onclick = e => { if (e.target === lb) lb.remove(); };
  const img = document.createElement('img');
  img.src = src;
  lb.appendChild(img);
  const close = document.createElement('button');
  close.className = 'lightbox-close';
  close.innerHTML = '✕';
  close.onclick = () => lb.remove();
  lb.appendChild(close);
  document.body.appendChild(lb);
  const esc = e => { if (e.key === 'Escape') { lb.remove(); document.removeEventListener('keydown', esc); } };
  document.addEventListener('keydown', esc);
}

function fmtLang(d) { return d.toLocaleDateString('de-DE', { day: 'numeric', month: 'long', year: 'numeric' }); }
function fmtKurz(d) { return d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric' }); }
