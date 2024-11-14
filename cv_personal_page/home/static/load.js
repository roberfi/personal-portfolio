const container = document.getElementById("container");
const overlay = document.getElementById("overlay");

const progress_bar = document.getElementById("progress-bar");
const navigation_bar = document.querySelector("#nav-bar");

// Method to scroll smoothly into element
function smoothScroll(target, push = true)
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

function removeLoadingClass()
{
    document.body.className = document.body.className.replace(/\bjs-loading\b/, '');
}

// Page load event, remove loading class to display body and scroll into hash element
function onLoad()
{
    setTimeout(() =>
    {
        container.scrollTo(0, 0);
        removeLoadingClass();

        if (window.location.hash)
        {
            setTimeout(() =>
            {
                smoothScroll(window.location.hash, false);
            }, 300);
        }
    }, 10);
}

// Clicks on buttons
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

/******** Navigation buttons *********/
const navigationMenuButton = document.querySelector("#navigation-menu-button");
const navigationMenu = document.querySelector("#navigation-menu");
const navigationMenuLinks = document.querySelectorAll("#navigation-menu > ul > li > a");

const maxMdHiddenClassName = "max-md:hidden";

function hideNavigationMenu()
{
    if (!navigationMenu.classList.contains(maxMdHiddenClassName))
    {
        navigationMenu.classList.add(maxMdHiddenClassName);
    }
}

navigationMenuButton.addEventListener("click", () =>
{
    navigationMenu.classList.toggle(maxMdHiddenClassName);
});

navigationMenuLinks.forEach((element) =>
{
    element.addEventListener("click", hideNavigationMenu);
});

/******** Language buttons *********/
const languageMenuButton = document.querySelector("#language-menu-button");
const languageMenu = document.querySelector("#language-menu");
const languageMenuLinks = document.querySelectorAll("#language-menu > ul > li > a");

const hiddenClassName = "hidden";

function hideLanguageMenu()
{
    if (!languageMenu.classList.contains(hiddenClassName))
    {
        languageMenu.classList.add(hiddenClassName);
    }
}

languageMenuButton.addEventListener("click", () =>
{
    languageMenu.classList.toggle(hiddenClassName);
});

languageMenuLinks.forEach((element) =>
{
    element.addEventListener("click", hideLanguageMenu);
});

function changeLanguage(url, languageCode)
{
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            'X-CSRFToken': csrftoken,
        },
        body: new URLSearchParams(
            {
                "language": languageCode,
                "next": window.location.pathname.replace(/^\/(en|es)/, ""),
            }
        )
    }).then(response =>
    {
        if (response.redirected)
        {
            let redirect_url = response.url;

            if (window.location.hash)
            {
                redirect_url += window.location.hash;
            }

            window.location.href = redirect_url;
        }
    });
}

window.changeLanguage = changeLanguage;

if (document.readyState === 'complete')
{
    onLoad();
} else
{
    window.addEventListener('load', onLoad);
}
