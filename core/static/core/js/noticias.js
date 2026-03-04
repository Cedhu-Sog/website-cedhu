function openModal(img) {
  const modal = document.getElementById('imgModal');
  const modalImg = document.getElementById('modalImg');
  modal.style.display = 'flex';
  modalImg.src = img.src;
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  const modal = document.getElementById('imgModal');
  modal.style.display = 'none';
  document.body.style.overflow = '';
}

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') closeModal();
});