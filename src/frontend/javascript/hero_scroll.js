// Drives a `--hero-progress` custom property (0 → 1) on the scroll container as
// the hero scrolls away. CSS uses it to progressively fade out the hero and
// fade in the home identity bar, instead of a binary toggle.

export function initHeroScroll() {
  const container = document.getElementById("container");
  const hero = document.getElementById("home");

  if (!container || !hero) {
    return;
  }

  const update = () => {
    // Complete the transition over ~65% of the hero's height so the bar is
    // fully formed before the hero has finished scrolling off.
    const distance = hero.offsetHeight * 0.65 || 1;
    const progress = Math.min(Math.max(container.scrollTop / distance, 0), 1);
    container.style.setProperty("--hero-progress", progress.toFixed(3));
  };

  container.addEventListener("scroll", update, { passive: true });
  update();
}
