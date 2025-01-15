import { navigationBar, navigationMenuLinks } from "./navigation_bar.js";

export const container = document.getElementById("container");
const progressBar = document.getElementById("progress-bar");

// Method to scroll smoothly into element
export function smoothScroll(target) {
  const element = document.querySelector(target);
  const navBarHeight = progressBar.clientHeight + navigationBar.clientHeight;

  if (element) {
    container.scrollTo({
      top: element.offsetTop - navBarHeight,
      behavior: "smooth",
    });
  }
}

export function initScroll() {
  // Event on scroll to change overlay opacity
  container.addEventListener("scroll", () => {
    // Change the section on the 1/4 of the container
    const containerScrollPosition =
      container.scrollTop + container.offsetTop + container.clientHeight / 4;

    // Set the progress of the progress bar
    progressBar.value =
      (container.scrollTop /
        (container.scrollHeight - container.clientHeight)) *
      100;

    // Change active section when corresponds
    Array.from(navigationMenuLinks).every((link) => {
      const sectionHash = link.getAttribute("href");
      const section = document.querySelector(sectionHash);

      if (
        section.offsetTop <= containerScrollPosition &&
        section.offsetTop + section.clientHeight > containerScrollPosition
      ) {
        // Update button state
        navigationMenuLinks.forEach((other_link) => {
          other_link.classList.remove("active");
          //other_link.blur(); // Remove the focus
        });
        link.classList.add("active");

        // Update text of title for mobiles
        document.getElementById("active-section-title").textContent =
          link.textContent;

        // Update hash
        if (sectionHash != window.location.hash) {
          history.replaceState(null, null, sectionHash);
        }

        return false;
      }

      return true;
    });
  });
}
