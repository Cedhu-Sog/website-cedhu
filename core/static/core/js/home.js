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


const track = document.querySelector('.hero-track');
const slides = document.querySelectorAll('.hero-slide');
const leftArrow = document.querySelector('.hero-arrow.left');
const rightArrow = document.querySelector('.hero-arrow.right');

let currentIndex = 0;
let autoplayInterval;
let player;
let isPaused = false;
let startX = 0;
let isDragging = false;
const imageDuration = 5000;

// ----------------
// YOUTUBE API
// ----------------
function onYouTubeIframeAPIReady() {
  player = new YT.Player('heroVideo', {
    events: {
      'onStateChange': onPlayerStateChange
    }
  });
}

function onPlayerStateChange(event) {
  if (event.data === YT.PlayerState.ENDED) {
    goToSlide(0);
  }
}

// ----------------
// SLIDE CONTROL
// ----------------
function updateSlidePosition() {
  track.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function goToSlide(index) {
  stopAutoplay();
  currentIndex = index;
  updateSlidePosition();

  const type = slides[currentIndex].dataset.type;

  if (type === "video") {
    player.playVideo();
  } else {
    if (player) player.pauseVideo();
    startAutoplay();
  }
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % slides.length;
  goToSlide(currentIndex);
}

function prevSlide() {
  currentIndex = (currentIndex - 1 + slides.length) % slides.length;
  goToSlide(currentIndex);
}

// ----------------
// AUTOPLAY IMAGES
// ----------------
function startAutoplay() {
  autoplayInterval = setInterval(() => {
    nextSlide();
  }, imageDuration);
}

function stopAutoplay() {
  clearInterval(autoplayInterval);
}

// ----------------
// PAUSA AL MANTENER
// ----------------
function pauseAll() {
  isPaused = true;
  stopAutoplay();
  if (player) player.pauseVideo();
}

function resumeAll() {
  if (!isPaused) return;
  isPaused = false;

  if (slides[currentIndex].dataset.type === "video") {
    player.playVideo();
  } else {
    startAutoplay();
  }
}

document.querySelector('.hero').addEventListener('mousedown', pauseAll);
document.querySelector('.hero').addEventListener('mouseup', resumeAll);
document.querySelector('.hero').addEventListener('touchstart', pauseAll);
document.querySelector('.hero').addEventListener('touchend', resumeAll);

// ----------------
// FLECHAS
// ----------------
rightArrow.addEventListener('click', nextSlide);
leftArrow.addEventListener('click', prevSlide);

// ----------------
// SWIPE MOBILE
// ----------------
document.querySelector('.hero').addEventListener('touchstart', e => {
  startX = e.touches[0].clientX;
});

document.querySelector('.hero').addEventListener('touchend', e => {
  let endX = e.changedTouches[0].clientX;
  let diff = startX - endX;

  if (Math.abs(diff) > 50) {
    if (diff > 0) nextSlide();
    else prevSlide();
  }
});

// INICIAR
startAutoplay();


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

