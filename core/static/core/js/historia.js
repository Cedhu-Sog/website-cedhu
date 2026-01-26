document.addEventListener("DOMContentLoaded", () => {
  const timelineData = {
    1988: "En febrero de 1988, MARTHA HELENA GAITÁN GARCÍA fundó en Sogamoso el JARDÍN MATERNO INFANTIL TRIBILÍN. Con un equipo excepcional, inició el proceso de adaptación y construcción de aprendizajes para 20 Tribilines.",
    1996: "En 1996 se implementó la Básica Primaria y se propuso el cambio de razón social por CENTRO EDUCATIVO DE DESARROLLO HUMANO (CEDHU).",
    2001: "A finales de 2001, aprobado el cambio de razón social, se dio inicio a la Básica Secundaria con Profundización en inglés y Sistemas.",
    2003: "Finalizando el 2003, el Dr. JUAN CARLOS RUÍZ FAJARDO se unió al proyecto, aportando la Profundización en Valores del Ser y orientando el Proyecto Educativo hacia la búsqueda de la Felicidad a través del fortalecimiento de valores.",
    2005: "En 2005 se completó el ciclo con la Educación Media, dando inicio al CENTRO DE DESARROLLO HUMANO CEDHU. En 2006 se graduó la Primera Promoción de Bachilleres Cedhuistas, alcanzando Nivel Muy Superior (A+) en las Pruebas ICFES – SABER 11°.",
    2007: "Desde 2007, la Señora CELIA ELENA FAJARDO GARAVITO asumió el cargo de Administradora. Su gestión permitió innovar en procesos académicos, ampliar y adecuar la planta física, dotar Aulas Especializadas y mejorar las condiciones laborales del personal.",
    2019: "Desde 2019, los Bachilleres Cedhuistas son certificados con la Prueba TOEFL JUNIOR STANDARD, que mide habilidades en Listening, Reading y Language Form and Meaning.",
    actualidad:
      "Actualmente, el CEDHU es reconocido en la región como una institución pionera, vanguardista y de calidad, destacada por la riqueza en su servicio y la Calidad Humana de sus integrantes.",
  };

  const items = document.querySelectorAll(".timeline-item");
  const textEl = document.getElementById("timeline-text");
  const mobileDescriptions = document.querySelectorAll(".mobile-description");

  if (window.innerWidth <= 768) {
    mobileDescriptions[0].textContent = timelineData[items[0].dataset.year];
  }

  items.forEach((btn, index) => {
    btn.addEventListener("click", () => {
      // Quitar activo
      items.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      // Actualizar texto principal (versión escritorio)
      textEl.classList.add("fade-out");
      setTimeout(() => {
        textEl.textContent = timelineData[btn.dataset.year];
        textEl.classList.remove("fade-out");
      }, 300);

      // Mostrar en móvil
      mobileDescriptions.forEach((desc) => (desc.textContent = ""));
      if (window.innerWidth <= 768) {
        mobileDescriptions[index].textContent = timelineData[btn.dataset.year];
      }
    });
  });
});
