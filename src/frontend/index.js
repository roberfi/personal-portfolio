import "@fontsource/roboto";
import "./styles/main.css";

import { container, smoothScroll, initScroll } from "./javascript/scroll.js";
import { initNavigationBar } from "./javascript/navigation_bar.js";

window.addEventListener("load", () => {
  initNavigationBar();
  initScroll();

  // scroll into hash element
  setTimeout(() => {
    const initial_hash = window.location.hash;

    container.scrollTo(0, 0);

    if (initial_hash) {
      setTimeout(() => {
        smoothScroll(initial_hash);
      }, 300);
    }
  }, 10);
});
