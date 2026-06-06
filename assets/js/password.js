/* ============================================
   Sias Tagebuch – Passwort-Schutz
   ============================================ */

(function() {
  const CORRECT_PASSWORD = 'S0701Y0203C2110';
  const STORAGE_KEY = 'sias_tagebuch_auth';

  // Prüfen ob bereits in dieser Session authentifiziert
  function isAuthenticated() {
    return sessionStorage.getItem(STORAGE_KEY) === 'true';
  }

  // Passwort-Overlay erstellen
  function createOverlay() {
    const overlay = document.createElement('div');
    overlay.className = 'password-overlay';
    overlay.id = 'password-overlay';
    overlay.innerHTML = `
      <div class="password-box">
        <div class="password-icon">🔒</div>
        <h2>Willkommen</h2>
        <p>Bitte gib das Passwort ein, um Sias Tagebuch zu sehen.</p>
        <div class="password-input-group">
          <input type="password" class="password-input" id="password-input" placeholder="Passwort" autocomplete="off">
          <button class="password-btn" id="password-btn">Öffnen</button>
          <div class="password-error" id="password-error">Falsches Passwort – versuch es nochmal</div>
        </div>
        <div class="password-hint">✨ Ein Familien-Geheimnis</div>
      </div>
    `;
    document.body.appendChild(overlay);
    return overlay;
  }

  // Seite entsperren
  function unlockPage() {
    sessionStorage.setItem(STORAGE_KEY, 'true');
    const overlay = document.getElementById('password-overlay');
    if (overlay) {
      overlay.classList.add('hidden');
      setTimeout(() => {
        overlay.style.display = 'none';
      }, 600);
    }
    document.body.classList.add('protected');

    // Fokus auf den ersten Input oder Inhalt
    const firstInput = document.querySelector('main input, main a, main button');
    if (firstInput) firstInput.focus();
  }

  // Passwort prüfen
  function checkPassword() {
    const input = document.getElementById('password-input');
    const error = document.getElementById('password-error');
    
    if (input.value === CORRECT_PASSWORD) {
      unlockPage();
    } else {
      error.classList.add('visible');
      input.value = '';
      input.focus();
      // shake animation
      input.style.animation = 'shake 0.4s ease';
      setTimeout(() => { input.style.animation = ''; }, 400);
    }
  }

  // Shake-Animation für falsches Passwort
  const style = document.createElement('style');
  style.textContent = `
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      20% { transform: translateX(-8px); }
      40% { transform: translateX(8px); }
      60% { transform: translateX(-5px); }
      80% { transform: translateX(5px); }
    }
  `;
  document.head.appendChild(style);

  // Initialisieren
  if (isAuthenticated()) {
    // Bereits authorisiert – alles freigeben
    document.body.classList.add('protected');
  } else {
    // Overlay anzeigen
    const overlay = createOverlay();

    // Event-Listener (nachdem DOM geladen ist)
    document.addEventListener('DOMContentLoaded', function() {
      const input = document.getElementById('password-input');
      const btn = document.getElementById('password-btn');
      const error = document.getElementById('password-error');

      if (input) {
        input.focus();
        input.addEventListener('keydown', function(e) {
          if (e.key === 'Enter') {
            e.preventDefault();
            checkPassword();
          }
          // Fehler zurücksetzen bei neuer Eingabe
          if (error) error.classList.remove('visible');
        });
      }

      if (btn) {
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          checkPassword();
        });
      }
    });
  }
})();
