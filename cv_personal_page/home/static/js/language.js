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
}
