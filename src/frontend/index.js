import "@fontsource-variable/inter";
import "./styles/main.css";

import { initProgressBar } from "./javascript/progress_bar";
import { setupContactForm } from "./javascript/contact_form";
import { initStickyHeadings } from "./javascript/sticky_headings";

window.addEventListener("load", () => {
  initProgressBar();
  initStickyHeadings();
});

// Export for use in templates
export { setupContactForm };
