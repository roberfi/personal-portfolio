// Control of language menu buttons
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

export function initLanguage()
{
    languageMenuButton.addEventListener("click", () =>
    {
        languageMenu.classList.toggle(hiddenClassName);
    });

    languageMenuLinks.forEach((element) =>
    {
        element.addEventListener("click", hideLanguageMenu);
    });

    // Method to request language change
    window.changeLanguage = function (url, languageCode)
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
}
