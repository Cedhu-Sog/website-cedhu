// --- Botones "Ver más" ---
window.toggleMore = function (btn) {
  const more = btn.previousElementSibling;
  if (!more) return;
  const isOpen = more.style.display === 'block';
  more.style.display = isOpen ? 'none' : 'block';
  btn.textContent = isOpen ? 'Ver más' : 'Ver menos';
};

// --- Acordeón ---
(function () {
  const accordions = document.querySelectorAll('.accordion');
  accordions.forEach(acc => {
    const btn = acc.querySelector('.accordion-btn');
    const content = acc.querySelector('.accordion-content');
    if (!btn || !content) return;
    btn.addEventListener('click', () => {
      const open = content.classList.toggle('open');
      if (open) {
        const scrollHeight = content.scrollHeight + 36; // padding
        content.style.maxHeight = scrollHeight + 'px';
      } else {
        content.style.maxHeight = '0px';
      }
    });
  });
})();

// --- Flip de tarjetas del staff ---
(function () {
  document.querySelectorAll('.staff-card').forEach(card => {
    const toggle = () => card.classList.toggle('flipped');
    card.addEventListener('click', toggle);
    card.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggle();
      }
    });
  });
})();



// --- Espacios ---
document.addEventListener("DOMContentLoaded", () => {
  const galleryItems = document.querySelectorAll(".gallery-item");
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-img");
  const lightboxTitle = document.getElementById("lightbox-title");
  const closeBtn = document.getElementById("closeLightbox");

  galleryItems.forEach(item => {
    item.addEventListener("click", () => {
      const img = item.querySelector("img");
      const title = item.getAttribute("data-title");

      lightboxImg.src = img.src;
      lightboxImg.alt = img.alt;
      lightboxTitle.textContent = title;

      lightbox.classList.remove("hide");
    });
  });

  // Cerrar lightbox con botón
  closeBtn.addEventListener("click", () => {
    lightbox.classList.add("hide");
  });

  // Cerrar lightbox haciendo clic fuera del contenido
  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) {
      lightbox.classList.add("hide");
    }
  });

  // Cerrar con tecla ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      lightbox.classList.add("hide");
    }
  });
});

/* --- Himno --- */

// Asegúrate de que estas variables seleccionen los elementos correctos por su ID
const botonMusica = document.getElementById('botonMusica'); 
const musicaFondo = document.getElementById('musicaFondo');
let reproduciendo = false;

if (botonMusica && musicaFondo) {
    botonMusica.addEventListener('click', function() {
        if (!reproduciendo) {
            // Iniciar reproducción
            musicaFondo.play();
            // Añade la clase 'is-playing' al botón
            this.classList.add('is-playing'); 
            reproduciendo = true;
        } else {
            // Pausar reproducción
            musicaFondo.pause();
            // Elimina la clase 'is-playing' del botón
            this.classList.remove('is-playing'); 
            reproduciendo = false;
        }
    });

    // Opcional: Manejar el final de la canción automáticamente
    musicaFondo.addEventListener('ended', function() {
        botonMusica.classList.remove('is-playing');
        reproduciendo = false;
    });
}


// --- Animaciones al scroll solo hacia abajo ---
(function() {
  const animados = document.querySelectorAll(
    ".section h2, .section.alt h2, .section.comunicacion h2, .section.filosofia h2, .bandera-box h2, .uniforme-box h2, .lema-text h2, .mision-vision h2, .timeline h2, .staff-card-front h4"
  );

  animados.forEach(el => el.classList.add('animado-inicio'));

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        const el = entry.target;
        const index = Array.from(animados).indexOf(el);
        const delay = index * 0.05; 
        el.style.transitionDelay = `${delay}s`;
        el.classList.add('animado');
        el.classList.remove('animado-inicio');
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.15 });

  animados.forEach(el => observer.observe(el));
})();

// --- Tarjetas Principios ---
function toggleCard(card) {
  document.querySelectorAll('.principio-card').forEach(c => {
    if (c !== card) c.classList.remove('active');
  });
  card.classList.toggle('active');
}

function togglePrincipio(card) {
  const allCards = document.querySelectorAll('.principio-card');
  allCards.forEach(c => {
    if (c !== card) {
      c.classList.remove('expanded');
      c.querySelector('.principio-info').classList.remove('show');
    }
  });

  const info = card.querySelector('.principio-info');
  card.classList.toggle('expanded');
  info.classList.toggle('show');
}
