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

/* Use the tallest publication's copy to size matching 5:4 figure areas. */
(() => {
  if (!("ResizeObserver" in window)) return;
  const compact = window.matchMedia("(max-width: 1000px)");

  document.querySelectorAll(".publication-list").forEach((list) => {
    const cards = [...list.querySelectorAll(".publication-card")];
    const contents = cards.map((card) => card.querySelector(".publication-content"));
    if (!cards.length || contents.some((content) => !content)) return;
    let signature = "";
    let pending = false;

    function dimensions() {
      return cards.map((card, index) =>
        `${card.clientWidth}:${contents[index].getBoundingClientRect().height}`
      ).join(";");
    }

    function reset() {
      list.classList.remove("publication-list-dynamic");
      list.style.removeProperty("--publication-image-width");
      cards.forEach((card) => card.classList.remove("publication-card-dynamic"));
    }

    function layout() {
      pending = false;
      if (dimensions() === signature) return;
      reset();

      if (!compact.matches) {
        const available = Math.min(...cards.map((card) => card.clientWidth));
        const minimumTextWidth = 16 * parseFloat(getComputedStyle(document.documentElement).fontSize);
        let imageWidth = 0;
        let fitted = false;
        cards.forEach((card) => card.classList.add("publication-card-dynamic"));

        // Start with the widest text column and converge as its lines wrap.
        for (let attempt = 0; attempt < 24; attempt++) {
          list.style.setProperty("--publication-image-width", `${imageWidth}px`);
          const tallestHeight = Math.max(...contents.map((content) => content.getBoundingClientRect().height));
          const requiredWidth = tallestHeight * 5 / 4;
          if (requiredWidth > available - minimumTextWidth) break;
          if (Math.abs(requiredWidth - imageWidth) < .5) {
            list.style.setProperty("--publication-image-width", `${requiredWidth}px`);
            list.classList.add("publication-list-dynamic");
            fitted = true;
            break;
          }
          imageWidth = requiredWidth;
        }

        // Stack when a 5:4 figure would leave too little room for readable copy.
        if (!fitted) {
          reset();
        }
      }
      signature = dimensions();
    }

    function schedule() {
      if (pending) return;
      pending = true;
      requestAnimationFrame(layout);
    }

    const observer = new ResizeObserver(schedule);
    cards.forEach((card) => observer.observe(card));
    compact.addEventListener("change", () => {
      signature = "";
      schedule();
    });
    document.fonts?.ready.then(() => {
      signature = "";
      schedule();
    });
    layout();
  });
})();
