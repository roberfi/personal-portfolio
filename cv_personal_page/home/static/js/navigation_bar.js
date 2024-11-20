import { smoothScroll } from "./scroll.js";

export const navigation_bar = document.querySelector("#nav-bar");

// Control of navigation menu buttons
const navigationMenuButton = document.querySelector("#navigation-menu-button");
const navigationMenu = document.querySelector("#navigation-menu");
export const navigationMenuLinks = document.querySelectorAll("#navigation-menu > ul > li > a");

const maxMdHiddenClassName = "max-md:hidden";

function hideNavigationMenu()
{
    if (!navigationMenu.classList.contains(maxMdHiddenClassName))
    {
        navigationMenu.classList.add(maxMdHiddenClassName);
    }
}

export function initNavigationBar()
{
    // Clicks on navigation menu buttons
    document.addEventListener('click', (event) =>
    {
        const target = event.target;

        if (target.tagName === 'A' && target.hash && target.host === window.location.host)
        {
            event.preventDefault();
            history.pushState(null, '', target.href);
            smoothScroll(target.hash);
        }
    });

    // Changes in the history, like browser navigation buttons
    window.addEventListener('popstate', () =>
    {
        if (event.state && event.state.scrollTarget)
        {
            smoothScroll(event.state.scrollTarget, false);
        }
    });

    navigationMenuButton.addEventListener("click", () =>
    {
        navigationMenu.classList.toggle(maxMdHiddenClassName);
    });

    navigationMenuLinks.forEach((element) =>
    {
        element.addEventListener("click", hideNavigationMenu);
    });
}
