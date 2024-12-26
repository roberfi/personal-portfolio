import { smoothScroll } from "./scroll.js";

export const navigationBar = document.querySelector("#nav-bar");

// Control of navigation menu buttons
const navigationMenuButton = document.querySelector("#navigation-menu-button");
const navigationMenu = document.querySelector("#navigation-menu");
export const navigationMenuLinks =
  document.querySelectorAll("#navigation-menu a");

const maxMdHiddenClassName = "max-md:hidden";

function handleButtonClick(event) {
  const target = event.target;

  event.preventDefault();
  smoothScroll(target.hash);

  if (!navigationMenu.classList.contains(maxMdHiddenClassName)) {
    navigationMenu.classList.add(maxMdHiddenClassName);
  }
}

export function initNavigationBar() {
  navigationMenuButton.addEventListener("click", () => {
    navigationMenu.classList.toggle(maxMdHiddenClassName);
  });

  // Clicks on navigation menu buttons
  navigationMenuLinks.forEach((element) => {
    element.addEventListener("click", handleButtonClick);
  });
}
