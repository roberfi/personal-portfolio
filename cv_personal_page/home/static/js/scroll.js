import { navigation_bar } from "./navigation_bar.js";

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
        // Change class name to add opacity when scrolling down
        const rounded_percentage = Math.round(container.scrollTop / container.clientHeight * 10) * 10;
        const overlay_opacity = Math.min(Math.max(rounded_percentage, 10), 70);
        overlay.className = overlay.className.replace(/bg-base-100\/\d+/, "bg-base-100/" + overlay_opacity);

        // Set the progress of the progress bar
        progress_bar.value = (container.scrollTop / (container.scrollHeight - container.clientHeight)) * 100;
    });

}
