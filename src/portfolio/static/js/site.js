/* Progressive enhancement: sticky navigation and keyboard-friendly mobile menu. */
(() => {
  const menu = document.querySelector(".site-nav");
  const toggle = document.querySelector(".mobile-toggle");
  const links = [...document.querySelectorAll(".site-nav a")];
  if (!menu || !toggle) return;

  function closeMenu(returnFocus = false) {
    menu.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    if (returnFocus) toggle.focus();
  }

  function initMobileMenu() {
    toggle.addEventListener("click", () => {
      const opened = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(opened));
    });

    links.forEach((link) => link.addEventListener("click", () => closeMenu()));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menu.classList.contains("is-open")) closeMenu(true);
    });
    window.matchMedia("(max-width: 720px)").addEventListener("change", () => closeMenu());
    document.documentElement.classList.add("nav-enhanced");
  }

  function initSectionNavigation() {
    if ("IntersectionObserver" in window) {
      const sections = links
        .map((link) => document.querySelector(link.getAttribute("href")))
        .filter(Boolean);
      const visible = new Set();
      const observer = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) visible.add(entry.target);
            else visible.delete(entry.target);
          }
          const section = sections.find((section) => visible.has(section));
          if (!section) return;
          links.forEach((link) => link.removeAttribute("aria-current"));
          links.find((link) => link.hash === "#" + section.id)?.setAttribute("aria-current", "location");
        },
        { rootMargin: "-90px 0px -65% 0px", threshold: 0 }
      );
      sections.forEach((section) => observer.observe(section));
    }
  }
  initMobileMenu();
  initSectionNavigation();
})();
