import "./styles/main.css";

import { initProgressBar } from "./javascript/progress_bar";
import { setupContactForm } from "./javascript/contact_form";

window.addEventListener("load", () => {
  initProgressBar();
});

// Export for use in templates
export { setupContactForm };
