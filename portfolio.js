const menuToggle = document.getElementById('menuToggle');
const nav = document.getElementById('nav');
function closeMenu() { nav.classList.remove('show'); menuToggle.setAttribute('aria-expanded', 'false'); }
menuToggle.addEventListener('click', () => { menuToggle.setAttribute('aria-expanded', String(nav.classList.toggle('show'))); });
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
const lightbox = document.getElementById('lightbox');
const lightboxImage = document.getElementById('lightboxImage');
document.querySelectorAll('.open-lightbox').forEach(button => {
  button.addEventListener('click', () => {
    lightboxImage.src = button.dataset.image;
    lightboxImage.alt = button.closest('article').querySelector('img').alt;
    lightbox.showModal();
  });
});
document.getElementById('lightboxClose').addEventListener('click', () => lightbox.close());
lightbox.addEventListener('click', event => { if (event.target === lightbox) lightbox.close(); });
lightbox.addEventListener('close', () => lightboxImage.removeAttribute('src'));
