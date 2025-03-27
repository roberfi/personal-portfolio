import { smoothScroll } from "./scroll.js";

export const navigationBar = document.querySelector("#nav-bar");

// Control of navigation menu buttons
export const navigationMenuLinks = document.querySelectorAll("a.section-link");

function handleButtonClick(event) {
  const target = event.target;

  event.preventDefault();
  smoothScroll(target.hash);

  target.blur();
}

export function initNavigationBar() {
  // Clicks on navigation menu buttons
  navigationMenuLinks.forEach((element) => {
    element.addEventListener("click", handleButtonClick);
  });
}
