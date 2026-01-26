  document.addEventListener("DOMContentLoaded", () => {
    // ============================================
    // BARRA DE PROGRESO DE LECTURA - CEDHU
    // ============================================
    function updateReadingProgress() {
      const winScroll = document.documentElement.scrollTop;
      const height =
        document.documentElement.scrollHeight -
        document.documentElement.clientHeight;
      const scrolled = (winScroll / height) * 100;

      let progressBar = document.getElementById("reading-progress");
      if (!progressBar) {
        progressBar = document.createElement("div");
        progressBar.id = "reading-progress";
        document.body.prepend(progressBar);
      }
      progressBar.style.width = scrolled + "%";
    }

    // Crear estilos para la barra
    const style = document.createElement("style");
    style.textContent = `
    #reading-progress {
      position: fixed;
      top: 0;
      left: 0;
      height: 3px;
      background: linear-gradient(90deg, #10B65C 0%, #FFE600 100%);
      z-index: 9999;
      transition: width 0.15s ease-out;
      box-shadow: 0 2px 4px rgba(14, 168, 82, 0.25);
    }
  `;
    document.head.appendChild(style);

    // Escucha el scroll
    window.addEventListener("scroll", updateReadingProgress);
  });


/* ============================================
 HERO SLIDER - AUTO Y CON VIDEOS SINCRONIZADOS 
============================================ */

document.addEventListener("DOMContentLoaded", () => {
  const heroSlides = Array.from(
    document.querySelectorAll(".hero-slide .slide")
  );
  const heroDots = Array.from(document.querySelectorAll(".hero-slide .dot"));
  const toggleBtn = document.getElementById("heroToggle");

  let heroIndex = 0;
  let autoplayTimer = null;
  let isPaused = false;

  const AUTOPLAY_DELAY = 6000;

  if (!heroSlides.length || !heroDots.length) return;

  /* ==========================
     AUTOPLAY
  ========================== */

  function stopAutoplay() {
    clearTimeout(autoplayTimer);
    autoplayTimer = null;
  }

  function startAutoplay() {
    if (isPaused) return;

    stopAutoplay();
    autoplayTimer = setTimeout(() => {
      nextHeroSlide();
    }, AUTOPLAY_DELAY);
  }

  function nextHeroSlide() {
    const next = (heroIndex + 1) % heroSlides.length;
    showHeroSlide(next);
  }

  /* ==========================
     SLIDES
  ========================== */

  function showHeroSlide(n) {
    heroSlides.forEach((slide, i) => {
      const overlay = slide.querySelector(".overlay");
      const video = slide.querySelector("video");

      slide.classList.toggle("active", i === n);
      if (heroDots[i]) heroDots[i].classList.toggle("active", i === n);

      if (i === n) {
        if (overlay) {
          overlay.classList.remove("animate");
          void overlay.offsetWidth;
          overlay.classList.add("animate");
        }
        if (video && !isPaused) {
          video.currentTime = 0;
          video.play().catch(() => {});
        }
      } else {
        if (overlay) overlay.classList.remove("animate");
        if (video) {
          video.pause();
          video.onended = null;
        }
      }
    });

    heroIndex = n;

    const currentVideo = heroSlides[n].querySelector("video");

    if (currentVideo && !isPaused) {
      currentVideo.onended = () => nextHeroSlide();
    } else {
      startAutoplay();
    }
  }

  /* ==========================
     BOTÓN PLAY / PAUSE
  ========================== */

  toggleBtn.addEventListener("click", () => {
    isPaused = !isPaused;

    const video = heroSlides[heroIndex].querySelector("video");
    if (video) isPaused ? video.pause() : video.play().catch(() => {});

    toggleBtn.textContent = isPaused ? "▶" : "⏸";

    isPaused ? stopAutoplay() : startAutoplay();
  });

  /* ==========================
     DOTS
  ========================== */

  heroDots.forEach((dot, i) => {
    dot.addEventListener("click", () => showHeroSlide(i));
  });

  /* ==========================
     VISIBILIDAD
  ========================== */

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopAutoplay();
    else if (!isPaused) startAutoplay();
  });

  /* ==========================
     INIT
  ========================== */

  showHeroSlide(0);
});

/* ==========================
   CONTROL DE PAUSA / PLAY
========================== */

function pauseHero() {
  isPaused = true;
  stopAutoplay();

  const currentSlide = heroSlides[heroIndex];
  const video = currentSlide.querySelector("video");

  if (video) {
    video.pause();
  }

  toggleBtn.textContent = "▶";
  toggleBtn.setAttribute("aria-pressed", "true");
}

function playHero() {
  isPaused = false;

  const currentSlide = heroSlides[heroIndex];
  const video = currentSlide.querySelector("video");

  if (video) {
    video.play().catch(() => {});
  }

  toggleBtn.textContent = "⏸";
  toggleBtn.setAttribute("aria-pressed", "false");

  startAutoplay();
}

toggleBtn.addEventListener("click", () => {
  isPaused ? playHero() : pauseHero();
});

/* ============================================
   BOTONES DE SECCIONES INTERACTIVAS
   ============================================ */
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".hub-buttons button");
  const boxes = document.querySelectorAll(".contenido-box");

  if (!buttons.length || !boxes.length) return;

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      // Quitar "active" de todo
      buttons.forEach((b) => b.classList.remove("active"));
      boxes.forEach((box) => box.classList.remove("active"));

      // Activar el actual
      btn.classList.add("active");
      const target = btn.getAttribute("data-target");
      document.getElementById(target).classList.add("active");
    });
  });
});

/* himno */

// document.addEventListener('DOMContentLoaded', () => {
//     // ... tu código existente ...

//     const botonMusica = document.getElementById('botonMusica');
//     const musicaFondo = document.getElementById('musicaFondo');
//     let reproduciendo = false;

//     botonMusica.addEventListener('click', function() {
//         if (!reproduciendo) {
//             musicaFondo.play();
//             this.innerHTML = "Pause";
//             reproduciendo = true;
//         } else {
//             musicaFondo.pause();
//             this.innerHTML = "Play";
//             reproduciendo = false;
//         }
//     });

//     // Manejo de errores
//     musicaFondo.addEventListener('error', function(e) {
//         console.error('Error al reproducir la música:', e);
//     });
// });

document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".hub-buttons button");
  const boxes = document.querySelectorAll(".contenido-box");

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      // Remover clase active de todos los botones y contenidos
      buttons.forEach((b) => b.classList.remove("active"));
      boxes.forEach((box) => box.classList.remove("active"));

      // Activar el botón actual y su contenido relacionado
      btn.classList.add("active");
      const target = btn.getAttribute("data-target");
      document.getElementById(target).classList.add("active");
    });
  });
});

// niveles educativos
function toggleInfo(card) {
  const info = card.querySelector(".nivel-info");
  const expanded = card.classList.contains("expanded");

  // Cierra todas las demás tarjetas
  document.querySelectorAll(".nivel-card").forEach((c) => {
    c.classList.remove("expanded");
    c.querySelector(".nivel-info").classList.remove("show");
  });

  // Si no estaba expandida, la abre
  if (!expanded) {
    card.classList.add("expanded");
    info.classList.add("show");
  }
}



document.querySelectorAll(".streetview").forEach((map) => {
  /* DESKTOP: doble clic */
  map.addEventListener("dblclick", (e) => {
    e.preventDefault();
    map.classList.add("active");
  });

  /* MÓVIL: tap largo */
  let pressTimer;

  map.addEventListener("touchstart", () => {
    pressTimer = setTimeout(() => {
      map.classList.add("active");
    }, 600); // tiempo de tap largo (ms)
  });

  map.addEventListener("touchend", () => {
    clearTimeout(pressTimer);
  });

  map.addEventListener("touchmove", () => {
    clearTimeout(pressTimer); // si hace scroll, no activa
  });
});

/* Desactivar al tocar fuera */
document.addEventListener("click", (e) => {
  document.querySelectorAll(".streetview.active").forEach((map) => {
    if (!map.contains(e.target)) {
      map.classList.remove("active");
    }
  });
});

/* Sección de noticias */

function openModal(img) {
  const modal = document.getElementById("imgModal");
  const modalImg = document.getElementById("modalImg");
  modal.style.display = "flex";
  modalImg.src = img.src;
}

function closeModal() {
  document.getElementById("imgModal").style.display = "none";
}

alert("JS cargado");