// Reveals each `c-page-heading` compact bar once its expanded title has
// scrolled above the top of the scroll container, pinning it under the navbar.

export function initStickyHeadings() {
  const root = document.getElementById("container");

  if (!root) {
    return;
  }

  document.querySelectorAll("[data-compact-bar]").forEach((bar) => {
    const key = bar.dataset.heading;
    const sentinel = root.querySelector(
      `[data-heading-sentinel][data-heading="${key}"]`,
    );

    if (!sentinel) {
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        // Stuck once the sentinel sits entirely above the container's top edge.
        const stuck =
          entry.boundingClientRect.bottom <=
          root.getBoundingClientRect().top + 1;
        bar.classList.toggle("is-stuck", stuck);
      },
      { root, threshold: [0, 1] },
    );

    observer.observe(sentinel);
  });
}
