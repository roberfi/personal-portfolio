const container = document.getElementById("container");
const overlay = document.getElementById("overlay");

const progress_bar = document.getElementById("progress-bar");

// Method to scroll smoothly into element
function smoothScroll(target, push = true)
{
    const element = document.querySelector(target);

    if (element)
    {
        if (push)
        {
            history.pushState({ scrollTarget: target }, '', target);
        }
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
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
            }, 100);
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
    } else
    {
        handleHashChange();
    }
});


// Event on scroll to change overlay opacity
container.addEventListener("scroll", () =>
{
    // Change class name to add opacity when scrolling down
    overlay.className = overlay.className.replace(/bg-base-100\/\d+/, "bg-base-100/" + (container.scrollTop > 0 ? 60 : 10));

    // Set the progress of the progress bar
    progress_bar.value = (container.scrollTop / (container.scrollHeight - container.clientHeight)) * 100;
});

if (document.readyState === 'complete')
{
    onLoad();
} else
{
    window.addEventListener('load', onLoad);
}
