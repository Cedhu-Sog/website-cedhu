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
 HERO SLIDER - DESLIZAMIENTO LATERAL
============================================ */

document.addEventListener("DOMContentLoaded", () => {
  const hero = document.querySelector(".hero-slide");
  const slidesTrack = hero?.querySelector(".slides-track");
  const heroSlides = Array.from(hero?.querySelectorAll(".slide") || []);
  const heroDots = Array.from(hero?.querySelectorAll(".dot") || []);
  const YT_IFRAME_SELECTOR = "iframe[src*='youtube.com/embed']";

  if (!hero || !slidesTrack || !heroSlides.length) return;

  let heroIndex = 0;
  let youtubePlayer = null;
  let youtubeIframe = null;
  let youtubeApiReadyPromise = null;

  function isYoutubeSlide(slide) {
    return Boolean(slide && slide.querySelector(YT_IFRAME_SELECTOR));
  }

  function getCurrentSlide() {
    return heroSlides[heroIndex];
  }

  function ensureYouTubeApi() {
    if (window.YT && window.YT.Player) return Promise.resolve(window.YT);
    if (youtubeApiReadyPromise) return youtubeApiReadyPromise;

    youtubeApiReadyPromise = new Promise((resolve) => {
      const previousReady = window.onYouTubeIframeAPIReady;
      window.onYouTubeIframeAPIReady = () => {
        if (typeof previousReady === "function") previousReady();
        resolve(window.YT);
      };

      if (!document.querySelector("script[src='https://www.youtube.com/iframe_api']")) {
        const tag = document.createElement("script");
        tag.src = "https://www.youtube.com/iframe_api";
        document.head.appendChild(tag);
      }
    });

    return youtubeApiReadyPromise;
  }

  function initYouTubePlayer() {
    if (youtubePlayer || !youtubeIframe) return;

    ensureYouTubeApi().then(() => {
      if (youtubePlayer || !youtubeIframe) return;
      youtubePlayer = new window.YT.Player(youtubeIframe);
    });
  }

  function pauseSlideMedia(slide) {
    if (!slide) return;

    const video = slide.querySelector("video");
    if (video) video.pause();

    if (isYoutubeSlide(slide) && youtubePlayer && typeof youtubePlayer.pauseVideo === "function") {
      youtubePlayer.pauseVideo();
    }
  }

  function playSlideMedia(slide) {
    if (!slide) return;

    const video = slide.querySelector("video");
    if (video) {
      video.play().catch(() => {});
      return;
    }

    if (isYoutubeSlide(slide)) {
      if (!youtubePlayer) {
        initYouTubePlayer();
        return;
      }
      if (typeof youtubePlayer.playVideo === "function") youtubePlayer.playVideo();
    }
  }

  function scrollToSlide(index) {
    const clamped = Math.max(0, Math.min(index, heroSlides.length - 1));
    const target = heroSlides[clamped];
    if (!target) return;

    slidesTrack.scrollTo({ left: target.offsetLeft, behavior: "smooth" });
  }

  function setActiveSlide(index) {
    heroSlides.forEach((slide, i) => {
      slide.classList.toggle("active", i === index);
      if (heroDots[i]) heroDots[i].classList.toggle("active", i === index);
      if (i !== index) pauseSlideMedia(slide);
    });

    heroIndex = index;
    playSlideMedia(getCurrentSlide());
  }

  function updateFromScroll() {
    const nextIndex = Math.round(slidesTrack.scrollLeft / slidesTrack.clientWidth);
    if (nextIndex !== heroIndex && nextIndex >= 0 && nextIndex < heroSlides.length) {
      setActiveSlide(nextIndex);
    }
  }

  heroDots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
      scrollToSlide(i);
      setActiveSlide(i);
    });
  });

  slidesTrack.addEventListener("scroll", () => {
    window.requestAnimationFrame(updateFromScroll);
  });

  youtubeIframe = hero.querySelector(YT_IFRAME_SELECTOR);
  if (youtubeIframe) initYouTubePlayer();

  setActiveSlide(0);
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
