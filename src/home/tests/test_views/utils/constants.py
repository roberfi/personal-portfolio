from __future__ import annotations

from datetime import date

from utils.test_utils.constants import Language

# Home ids
HOME_ID = "home"
PERSONAL_INFO_NAME_ID = "personal-info-name"
PERSONAL_INFO_TITLE_ID = "personal-info-title"
PERSONAL_INFO_INTRODUCTION_ID = "personal-info-introduction"
PERSONAL_INFO_TECHNOLOGIES_ID = "personal-info-technologies"
ABOUT_ME_BUTTON_ID = "about-me-button"
ABOUT_ME_MODAL_ID = "about_me_modal"
ABOUT_ME_ID = "about-me"
ABOUT_ME_TITLE_ID = "about-me-title"
PERSONAL_INFO_BIOGRAPHY_ID = "personal-info-biography"

# My Career ids
MY_CAREER_ID = "my-career"
MY_CAREER_TITLE_ID = "my-career-title"
EXPERIENCES_LIST_ID = "experiences-list"
EXPERIENCE_ITEM_ID_TEMPLATE = "experience-{id}-item"
EXPERIENCE_PERIOD_ID_TEMPLATE = "experience-{id}-period"
EXPERIENCE_DURATION_ID_TEMPLATE = "experience-{id}-duration"
EXPERIENCE_TITLE_ID_TEMPLATE = "experience-{id}-title"
EXPERIENCE_COMPANY_ID_TEMPLATE = "experience-{id}-company"
EXPERIENCE_LOCATION_ID_TEMPLATE = "experience-{id}-location"
EXPERIENCE_TECHNOLOGIES_ID_TEMPLATE = "experience-{id}-technologies"
EXPERIENCE_MORE_BUTTON_ID_TEMPLATE = "experience-{id}-more-button"
EXPERIENCE_MODAL_ID_TEMPLATE = "experience_{id}_modal"
MODAL_EXPERIENCE_PERIOD_ID_TEMPLATE = "modal-experience-{id}-period"
MODAL_EXPERIENCE_DURATION_ID_TEMPLATE = "modal-experience-{id}-duration"
MODAL_EXPERIENCE_TITLE_ID_TEMPLATE = "modal-experience-{id}-title"
MODAL_EXPERIENCE_COMPANY_ID_TEMPLATE = "modal-experience-{id}-company"
MODAL_EXPERIENCE_LOCATION_ID_TEMPLATE = "modal-experience-{id}-location"
MODAL_EXPERIENCE_TECHNOLOGIES_ID_TEMPLATE = "modal-experience-{id}-technologies"
MODAL_EXPERIENCE_DESCRIPTION_ID_TEMPLATE = "modal-experience-{id}-description"
SUBPROJECTS_ID_TEMPLATE = "experience-{experience_id}-subprojects"
SUBPROJECT_TITLE_ID_TEMPLATE = "experience-{experience_id}-subproject-{subproject_id}-title"
SUBPROJECT_CLIENT_ID_TEMPLATE = "experience-{experience_id}-subproject-{subproject_id}-client"
SUBPROJECT_PERIOD_ID_TEMPLATE = "experience-{experience_id}-subproject-{subproject_id}-period"
SUBPROJECT_DURATION_ID_TEMPLATE = "experience-{experience_id}-subproject-{subproject_id}-duration"
SUBPROJECT_TECHNOLOGIES_ID_TEMPLATE = "experience-{experience_id}-subproject-{subproject_id}-technologies"
SUBPROJECT_DESCRIPTION_ID_TEMPLATE = "experience-{experience_id}-subproject-{subproject_id}-description"

# Footer ids
FOOTER_ID = "footer"
LEGAL_AND_PRIVACY_ID = "legal-and-privacy"
LEGAL_AND_PRIVACY_TITLE_ID = "legal-and-privacy-title"
LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE = "legal-and-privacy-{id}-link"
LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE = "legal_and_privacy_{id}_modal"
LEGAL_AND_PRIVACY_TITLE_ID_TEMPLATE = "legal-and-privacy-{id}-title"
LEGAL_AND_PRIVACY_TEXT_ID_TEMPLATE = "legal-and-privacy-{id}-text"
FOLLOW_ME_LINKS_ID = "follow-me-links"
FOLLOW_ME_LINKS_TITLE_ID = "follow-me-links-title"
FOLLOW_ME_LINK_CONTAINER_ID_TEMPLATE = "follow-me-link-{id}-container"
FOLLOW_ME_LINK_ID_TEMPLATE = "follow-me-link-{id}"

# About me texts
ABOUT_ME_TITLE = {
    Language.ENGLISH: "About me",
    Language.SPANISH: "Sobre mí",
}
ABOUT_ME_BUTTON_TEXT = {
    Language.ENGLISH: "More about me",
    Language.SPANISH: "Más sobre mí",
}


# My Career texts
MY_CAREER_TITLE = {
    Language.ENGLISH: "My Experience",
    Language.SPANISH: "Mi Experiencia",
}

# Personal Info data
PERSONAL_INFO_NAME = "Test Name"
PERSONAL_INFO_TITLE = {
    Language.ENGLISH: "Test title",
    Language.SPANISH: "Título de prueba",
}
PERSONAL_INFO_INTRODUCTION = {
    Language.ENGLISH: "Test introduction",
    Language.SPANISH: "Introducción de prueba",
}
PERSONAL_INFO_BIOGRAPHY = {
    Language.ENGLISH: "Test biography",
    Language.SPANISH: "Biografía de prueba",
}

# Technologies data
TECHNOLOGY_1 = {
    Language.ENGLISH: "Test Technology 1",
    Language.SPANISH: "Tecnología de Prueba 1",
}
TECHNOLOGY_2 = {
    Language.ENGLISH: "Test Technology 2",
    Language.SPANISH: "Tecnología de Prueba 2",
}
TECHNOLOGY_3 = {
    Language.ENGLISH: "Test Technology 3",
    Language.SPANISH: "Tecnología de Prueba 3",
}
TECHNOLOGY_4 = {
    Language.ENGLISH: "Test Technology 4",
    Language.SPANISH: "Tecnología de Prueba 4",
}

# Experiences data
EXPERIENCE_1_TITLE = {
    Language.ENGLISH: "Experience 1",
    Language.SPANISH: "Experiencia 1",
}
EXPERIENCE_1_LOCATION = {
    Language.ENGLISH: "Test Location 1",
    Language.SPANISH: "Ubicación de prueba 1",
}
EXPERIENCE_1_COMPANY = "Test Company 1"
EXPERIENCE_1_DESCRIPTION = {
    Language.ENGLISH: "Test description 1",
    Language.SPANISH: "Descripción de prueba 1",
}
EXPERIENCE_1_START_DATE = date(2021, 1, 1)
EXPERIENCE_1_END_DATE = date(2022, 3, 24)
EXPERIENCE_1_PERIOD = {
    Language.ENGLISH: "Jan, 2021 - Mar, 2022",
    Language.SPANISH: "Ene, 2021 - Mar, 2022",
}
EXPERIENCE_1_DURATION = {
    Language.ENGLISH: "(1 year, 2 months)",
    Language.SPANISH: "(1 año, 2 meses)",
}

EXPERIENCE_2_TITLE = {
    Language.ENGLISH: "Experience 2",
    Language.SPANISH: "Experiencia 2",
}
EXPERIENCE_2_LOCATION = {
    Language.ENGLISH: "Test Location 2",
    Language.SPANISH: "Ubicación de prueba 2",
}
EXPERIENCE_2_COMPANY = "Test Company 2"
EXPERIENCE_2_DESCRIPTION = {
    Language.ENGLISH: "Test description 2",
    Language.SPANISH: "Descripción de prueba 2",
}
EXPERIENCE_2_START_DATE = date(2022, 4, 1)
EXPERIENCE_2_PERIOD = {
    Language.ENGLISH: "Apr, 2022 - Present",
    Language.SPANISH: "Abr, 2022 - Actualmente",
}
EXPERIENCE_2_DURATION = {
    Language.ENGLISH: "(2 years, 3 months)",
    Language.SPANISH: "(2 años, 3 meses)",
}

EXPECTED_NUMBER_OF_EXPERIENCES = 2

# SubProjects data
SUBPROJECT_1_TITLE = {
    Language.ENGLISH: "SubProject 1",
    Language.SPANISH: "Subproyecto 1",
}
SUBPROJECT_1_CLIENT = "Test Client 1"
SUBPROJECT_1_DESCRIPTION = {
    Language.ENGLISH: "Test subproject description 1",
    Language.SPANISH: "Descripción de prueba del subproyecto 1",
}
SUBPROJECT_1_START_DATE = EXPERIENCE_2_START_DATE
SUBPROJECT_1_END_DATE = date(2023, 7, 30)
SUBPROJECT_1_PERIOD = {
    Language.ENGLISH: "Apr, 2022 - Jul, 2023",
    Language.SPANISH: "Abr, 2022 - Jul, 2023",
}
SUBPROJECT_1_DURATION = {
    Language.ENGLISH: "(1 year, 3 months)",
    Language.SPANISH: "(1 año, 3 meses)",
}
SUBPROJECT_1_TECHNOLOGIES = (
    TECHNOLOGY_1,
    TECHNOLOGY_3,
)
SUBPROJECT_2_TITLE = {
    Language.ENGLISH: "SubProject 2",
    Language.SPANISH: "Subproyecto 2",
}
SUBPROJECT_2_DESCRIPTION = {
    Language.ENGLISH: "Test subproject description 2",
    Language.SPANISH: "Descripción de prueba del subproyecto 2",
}
SUBPROJECT_2_START_DATE = date(2023, 8, 1)
SUBPROJECT_2_PERIOD = {
    Language.ENGLISH: "Aug, 2023 - Present",
    Language.SPANISH: "Ago, 2023 - Actualmente",
}
SUBPROJECT_2_DURATION = {
    Language.ENGLISH: "(11 months)",
    Language.SPANISH: "(11 meses)",
}
SUBPROJECT_2_TECHNOLOGIES = (TECHNOLOGY_2,)

EXPECTED_NUMBER_OF_SUBPROJECTS_EXPERIENCE_2 = 2

# Mocked today date
MOCKED_TODAY = date(2024, 7, 15)

# Footer
LEGAL_AND_PRIVACY_TITLE = {
    Language.ENGLISH: "Legal & Privacy",
    Language.SPANISH: "Condiciones y Privacidad",
}

LEGAL_SECTION_1 = {
    Language.ENGLISH: "Legal Section 1",
    Language.SPANISH: "Sección Legal 1",
}
LEGAL_TEXT_1 = {
    Language.ENGLISH: "Legal Text 1",
    Language.SPANISH: "Texto Legal 1",
}

LEGAL_SECTION_2 = {
    Language.ENGLISH: "Legal Section 2",
    Language.SPANISH: "Sección Legal 2",
}
LEGAL_TEXT_2 = {
    Language.ENGLISH: "Legal Text 2",
    Language.SPANISH: "Texto Legal 2",
}

FOLLOW_ME_LINKS_TITLE = {
    Language.ENGLISH: "Follow Me",
    Language.SPANISH: "Sígueme",
}

FOLLOW_ME_LINK_NAME = "Test Name"
FOLLOW_ME_LINK = "https://test.com"
FOLLOW_ME_LINK_VIEW_BOX = "0 0 186 186"
FOLLOW_ME_LINK_PATH = (
    "M5,52.888h33.334c2.762,0,5-2.239,5-5V14.555c0-2.761-2.238-5-5-5H5c-2.762,0-5,2.239-5,5v33.333 "
    "C0,50.649,2.238,52.888,5,52.888z M10,19.555h23.334v23.333H10V19.555z M38.334,132.779H5c-2.762,0-5,2.239-5,"
    "5v33.334 c0,2.761,2.238,5,5,5h33.334c2.762,0,5-2.239,5-5v-33.334C43.334,135.018,41.096,132.779,38.334,132."
    "779z M33.334,166.112H10 v-23.334h23.334V166.112z M55.167,20.446c0-2.761,2.238-5,5-5h120.5c2.762,0,5,2.239,"
    "5,5s-2.238,5-5,5h-120.5 C57.405,25.446,55.167,23.208,55.167,20.446z M55.167,40.242c0-2.761,2.238-5,5-"
    "5h75c2.762,0,5,2.239,5,5s-2.238,5-5,5h-75 C57.405,45.242,55.167,43.003,55.167,40.242z M55.167,82.935c0-2."
    "761,2.238-5,5-5h96.5c2.762,0,5,2.239,5,5c0,2.761-2.238,5-5,5 h-96.5C57.405,87.935,55.167,85.696,55.167,82."
    "935z M55.167,102.731c0-2.761,2.238-5,5-5h75c2.762,0,5,2.239,5,5 c0,2.761-2.238,5-5,5h-75C57.405,107.731,"
    "55.167,105.493,55.167,102.731z M55.167,144.547c0-2.761,2.238-5,5-5h96.5 c2.762,0,5,2.239,5,5c0,2.761-2."
    "238,5-5,5h-96.5C57.405,149.547,55.167,147.309,55.167,144.547z M185.667,164.343 c0,2.761-2.238,5-5,5h-120."
    "5c-2.762,0-5-2.239-5-5c0-2.761,2.238-5,5-5h120.5C183.429,159.343,185.667,161.582,185.667,164.343z M52.093,"
    "56.566c-2.328-1.484-5.42-0.799-6.903,1.53l-8.329,13.071H5c-2.762,0-5,2.239-5,5V109.5c0,2.761,2.238,5,5,5h33."
    "334 c2.762,0,5-2.239,5-5V79.617L53.623,63.47C55.106,61.141,54.422,58.05,52.093,56.566z M30.488,81.166l-9."
    "124,14.319l-9.761-14.016 c-0.078-0.112-0.175-0.2-0.26-0.303H30.488z M10,96.666l5.455,7.834H10V96.666z "
    "M33.334,104.5h-5.856l5.856-9.19V104.5z"
)
