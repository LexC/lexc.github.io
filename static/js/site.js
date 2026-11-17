/* Progressive enhancement: sticky navigation and keyboard-friendly mobile menu. */
(() => {
  const menu = document.querySelector(".site-nav");
  const toggle = document.querySelector(".mobile-toggle");
  const links = [...document.querySelectorAll(".site-nav a")];
  if (!menu || !toggle) return;

  function closeMenu() {
    menu.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
  }

  toggle.addEventListener("click", () => {
    const opened = menu.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(opened));
  });

  links.forEach((link) => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });

  if ("IntersectionObserver" in window) {
    const sections = links
      .map((link) => document.querySelector(link.getAttribute("href")))
      .filter(Boolean);
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          links.forEach((link) => link.removeAttribute("aria-current"));
          const active = links.find((link) => link.hash === "#" + entry.target.id);
          if (active) active.setAttribute("aria-current", "location");
        }
      },
      { rootMargin: "-90px 0px -65% 0px", threshold: 0 }
    );
    sections.forEach((section) => observer.observe(section));
  }
})();
