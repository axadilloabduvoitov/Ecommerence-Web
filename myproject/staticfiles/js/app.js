document.addEventListener("DOMContentLoaded", () => {
  const menu = document.querySelector("[data-menu]");
  const links = document.querySelector("[data-nav-links]");
  if (menu && links) {
    menu.addEventListener("click", () => links.classList.toggle("open"));
  }
  document.querySelectorAll("[data-auto-hide]").forEach((el) => {
    setTimeout(() => { el.style.opacity = "0"; el.style.transition = ".3s"; setTimeout(() => el.remove(), 350); }, 3500);
  });
});
