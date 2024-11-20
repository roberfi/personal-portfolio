import { container, smoothScroll, initScroll } from "./scroll.js";
import { initLanguage } from "./language.js";
import { initNavigationBar } from "./navigation_bar.js";

window.addEventListener('load', () =>
{
    initNavigationBar();
    initLanguage();
    initScroll();

    // remove loading class to display body and scroll into hash element
    setTimeout(() =>
    {
        container.scrollTo(0, 0);

        // Remove loading class
        document.body.className = document.body.className.replace(/\bjs-loading\b/, '');

        if (window.location.hash)
        {
            setTimeout(() =>
            {
                smoothScroll(window.location.hash);
            }, 300);
        }
    }, 10);
});