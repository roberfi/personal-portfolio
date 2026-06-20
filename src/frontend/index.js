import "./styles/main.css";

import { initProgressBar } from "./javascript/progress_bar";
import { setupContactForm } from "./javascript/contact_form";
import { initStickyHeadings } from "./javascript/sticky_headings";
import { initHeroScroll } from "./javascript/hero_scroll";

window.addEventListener("load", () => {
  initProgressBar();
  initStickyHeadings();
  initHeroScroll();
});

// Export for use in templates
export { setupContactForm };
