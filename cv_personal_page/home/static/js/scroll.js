import { navigation_bar, navigationMenuLinks } from "./navigation_bar.js";

export const container = document.getElementById("container");
const progress_bar = document.getElementById("progress-bar");

// Method to scroll smoothly into element
export function smoothScroll(target, push = true)
{
    const element = document.querySelector(target);
    const navBarHeight = progress_bar.clientHeight + navigation_bar.clientHeight;

    if (element)
    {
        if (push)
        {
            history.pushState({ scrollTarget: target }, '', target);
        }

        container.scrollTo({
            top: element.offsetTop - navBarHeight,
            behavior: 'smooth'
        });
    }
}

const overlay = document.getElementById("overlay");

export function initScroll()
{
    // Event on scroll to change overlay opacity
    container.addEventListener("scroll", () =>
    {
        const containerScrollTop = container.scrollTop;
        const containerClientHeight = container.clientHeight;
        const containerOffsetTop = Math.ceil(container.getBoundingClientRect().top);

        // Change class name to add opacity when scrolling down
        const rounded_percentage = Math.round(containerScrollTop / containerClientHeight * 10) * 10;
        const overlay_opacity = Math.min(Math.max(rounded_percentage, 10), 70);
        overlay.className = overlay.className.replace(/bg-base-100\/\d+/, "bg-base-100/" + overlay_opacity);

        // Set the progress of the progress bar
        progress_bar.value = (containerScrollTop / (container.scrollHeight - containerClientHeight)) * 100;

        // Change active section when corresponds
        navigationMenuLinks.forEach((link) =>
        {
            const section = document.querySelector(link.getAttribute("href"));

            if (section.offsetTop <= (containerScrollTop + containerOffsetTop))
            {
                navigationMenuLinks.forEach((other_link) => other_link.classList.remove("btn-active"));
                link.classList.add("btn-active");
                document.getElementById("active-section-title").innerHTML = link.innerHTML;
            }
        });
    });

}
