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

# Home CTA ids
HOME_CTA_ID = "home-cta"
HOME_CTA_EYEBROW_ID = "home-cta-eyebrow"
HOME_CTA_TITLE_ID = "home-cta-title"
HOME_CTA_PRIMARY_ID = "home-cta-primary"

# Featured projects ids
FEATURED_PROJECTS_SECTION_ID = "featured-projects"
FEATURED_PROJECTS_TITLE_ID = "featured-projects-title"
FEATURED_PROJECTS_GRID_ID = "featured-projects-grid"
FEATURED_PROJECTS_SEE_ALL_ID = "featured-projects-see-all"
PROJECT_CARD_ID_TEMPLATE = "project-{id}-card"
PROJECT_TITLE_ID_TEMPLATE = "project-{id}-title"
PROJECT_SUMMARY_ID_TEMPLATE = "project-{id}-summary"
PROJECT_TECHNOLOGIES_ID_TEMPLATE = "project-{id}-technologies"
PROJECT_DETAIL_LINK_ID_TEMPLATE = "project-{id}-detail-link"

# Projects list page ids
PROJECTS_SECTION_ID = "projects"
PROJECTS_TITLE_ID = "projects-title"
PROJECTS_GRID_ID = "projects-grid"

# Project detail page ids
PROJECT_DETAIL_ID = "project-detail"
PROJECT_DETAIL_TITLE_ID = "project-detail-title"
PROJECT_DETAIL_BACK_LINK_ID = "project-detail-back-link"
PROJECT_DETAIL_TECHNOLOGIES_ID = "project-detail-technologies"
PROJECT_DETAIL_PROBLEM_ID = "project-detail-problem"
PROJECT_DETAIL_APPROACH_ID = "project-detail-approach"
PROJECT_DETAIL_OUTCOME_ID = "project-detail-outcome"

# Process steps ids
PROCESS_STEPS_SECTION_ID = "process-steps"
PROCESS_STEPS_TITLE_ID = "process-steps-title"
PROCESS_STEPS_LIST_ID = "process-steps-list"
PROCESS_STEP_CARD_ID_TEMPLATE = "process-step-{id}-card"
PROCESS_STEP_ICON_ID_TEMPLATE = "process-step-{id}-icon"
PROCESS_STEP_NUMBER_ID_TEMPLATE = "process-step-{id}-number"
PROCESS_STEP_TITLE_ID_TEMPLATE = "process-step-{id}-title"
PROCESS_STEP_DESCRIPTION_ID_TEMPLATE = "process-step-{id}-description"

# Services ids
SERVICES_SECTION_ID = "services"
SERVICES_TITLE_ID = "services-title"
SERVICES_GRID_ID = "services-grid"
SERVICE_CARD_ID_TEMPLATE = "service-{id}-card"
SERVICE_CARD_BODY_ID_TEMPLATE = "service-{id}-card-body"
SERVICE_ICON_ID_TEMPLATE = "service-{id}-icon"
SERVICE_TITLE_ID_TEMPLATE = "service-{id}-title"
SERVICE_DESCRIPTION_ID_TEMPLATE = "service-{id}-description"
SERVICE_MORE_BUTTON_ID_TEMPLATE = "service-{id}-more-button"
SERVICE_MODAL_ID_TEMPLATE = "service_{id}_modal"
MODAL_SERVICE_ICON_ID_TEMPLATE = "modal-service-{id}-icon"
MODAL_SERVICE_TITLE_ID_TEMPLATE = "modal-service-{id}-title"
MODAL_SERVICE_DESCRIPTION_ID_TEMPLATE = "modal-service-{id}-description"
MODAL_SERVICE_CONTACT_ID_TEMPLATE = "modal-service-{id}-contact"

# My Career ids
MY_CAREER_ID = "my-career"
MY_EXPERIENCE_TITLE_ID = "my-experience-title"
EXPERIENCES_LIST_ID = "experiences-list"
EXPERIENCE_ITEM_ID_TEMPLATE = "experience-{id}-item"
EXPERIENCE_PERIOD_ID_TEMPLATE = "experience-{id}-period"
EXPERIENCE_DURATION_ID_TEMPLATE = "experience-{id}-duration"
EXPERIENCE_TITLE_ID_TEMPLATE = "experience-{id}-title"
EXPERIENCE_INSTITUTION_ID_TEMPLATE = "experience-{id}-institution"
EXPERIENCE_LOCATION_ID_TEMPLATE = "experience-{id}-location"
EXPERIENCE_TECHNOLOGIES_ID_TEMPLATE = "experience-{id}-technologies"
EXPERIENCE_MORE_BUTTON_ID_TEMPLATE = "experience-{id}-more-button"
EXPERIENCE_MODAL_ID_TEMPLATE = "experience_{id}_modal"
MODAL_EXPERIENCE_PERIOD_ID_TEMPLATE = "modal-experience-{id}-period"
MODAL_EXPERIENCE_DURATION_ID_TEMPLATE = "modal-experience-{id}-duration"
MODAL_EXPERIENCE_TITLE_ID_TEMPLATE = "modal-experience-{id}-title"
MODAL_EXPERIENCE_INSTITUTION_ID_TEMPLATE = "modal-experience-{id}-institution"
MODAL_EXPERIENCE_LOCATION_ID_TEMPLATE = "modal-experience-{id}-location"
MODAL_EXPERIENCE_TECHNOLOGIES_ID_TEMPLATE = "modal-experience-{id}-technologies"
MODAL_EXPERIENCE_DESCRIPTION_ID_TEMPLATE = "modal-experience-{id}-description"
# Education ids
EDUCATION_TITLE_ID = "education-title"
EDUCATION_LIST_ID = "education-list"
EDUCATION_ITEM_ID_TEMPLATE = "education-{id}-item"
EDUCATION_PERIOD_ID_TEMPLATE = "education-{id}-period"
EDUCATION_DURATION_ID_TEMPLATE = "education-{id}-duration"
EDUCATION_TITLE_ID_TEMPLATE = "education-{id}-title"
EDUCATION_INSTITUTION_ID_TEMPLATE = "education-{id}-institution"
EDUCATION_LOCATION_ID_TEMPLATE = "education-{id}-location"
EDUCATION_MORE_BUTTON_ID_TEMPLATE = "education-{id}-more-button"
EDUCATION_MODAL_ID_TEMPLATE = "education_{id}_modal"
MODAL_EDUCATION_PERIOD_ID_TEMPLATE = "modal-education-{id}-period"
MODAL_EDUCATION_DURATION_ID_TEMPLATE = "modal-education-{id}-duration"
MODAL_EDUCATION_TITLE_ID_TEMPLATE = "modal-education-{id}-title"
MODAL_EDUCATION_INSTITUTION_ID_TEMPLATE = "modal-education-{id}-institution"
MODAL_EDUCATION_LOCATION_ID_TEMPLATE = "modal-education-{id}-location"
MODAL_EDUCATION_DESCRIPTION_ID_TEMPLATE = "modal-education-{id}-description"

# Footer ids
UPPER_FOOTER_ID = "upper-footer"
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

BOTTOM_FOOTER_ID = "bottom-footer"
SOURCE_CODE_NOTE_ID = "source-code-note"
GITHUB_REPO_LINK_ID = "github-repo-link"

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

EDUCATION_TITLE = {
    Language.ENGLISH: "Education",
    Language.SPANISH: "Educación",
}

# SEO texts
COMMON_META_KEYWORDS = {
    Language.ENGLISH: ("portfolio", "CV", "biography", "career"),
    Language.SPANISH: ("portfolio", "CV", "biografía", "carrera"),
}

HOME_VIEW_META_TITLE_TEMPLATE = {
    Language.ENGLISH: "{name} | {title}",
    Language.SPANISH: "{name} | {title}",
}
HOME_VIEW_META_DESCRIPTION_TEMPLATE = {
    Language.ENGLISH: "Personal web of {name}. {title} specialized in {technologies}",
    Language.SPANISH: "Página personal de {name}. {title} especializado en {technologies}",
}


MY_CAREER_VIEW_META_TITLE = {
    Language.ENGLISH: "My Career | Professional Experience & Education",
    Language.SPANISH: "Mi Carrera | Experiencia Profesional y Educación",
}

PROJECTS_VIEW_META_TITLE = {
    Language.ENGLISH: "Projects | Portfolio",
    Language.SPANISH: "Proyectos | Portfolio",
}
PROJECTS_VIEW_META_DESCRIPTION = {
    Language.ENGLISH: "Browse all my projects — problem, approach, and outcomes.",
    Language.SPANISH: "Explora todos mis proyectos — problema, enfoque y resultados.",
}
PROJECTS_VIEW_META_KEYWORDS = {
    Language.ENGLISH: ("projects", "software development", "case studies"),
    Language.SPANISH: ("proyectos", "desarrollo de software", "casos de estudio"),
}

PROJECT_DETAIL_VIEW_META_TITLE_TEMPLATE = {
    Language.ENGLISH: "{title} | Portfolio",
    Language.SPANISH: "{title} | Portfolio",
}
MY_CAREER_VIEW_META_DESCRIPTION = {
    Language.ENGLISH: (
        "Professional experience and educational background."
        " View my complete career history, work experience, and academic qualifications."
    ),
    Language.SPANISH: (
        "Experiencia profesional y formación académica."
        " Consulta mi historial profesional completo, experiencia laboral y cualificaciones académicas."
    ),
}
MY_CAREER_VIEW_META_KEYWORDS = {
    Language.ENGLISH: ("experience", "education", "professional background", "work history"),
    Language.SPANISH: ("experiencia", "educación", "trayectoria profesional", "historia laboral"),
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

# Projects list page texts
PROJECTS_SECTION_TITLE = {
    Language.ENGLISH: "Projects",
    Language.SPANISH: "Proyectos",
}

# Featured projects data
FEATURED_PROJECTS_SECTION_TITLE = {
    Language.ENGLISH: "Featured projects",
    Language.SPANISH: "Proyectos destacados",
}
FEATURED_PROJECTS_SEE_ALL_TEXT = {
    Language.ENGLISH: "See all projects",
    Language.SPANISH: "Ver todos los proyectos",
}

PROJECT_1_TITLE = {
    Language.ENGLISH: "Project 1",
    Language.SPANISH: "Proyecto 1",
}
PROJECT_1_SLUG = "project-1"
PROJECT_1_SUMMARY = {
    Language.ENGLISH: "Project 1 summary",
    Language.SPANISH: "Resumen del proyecto 1",
}
PROJECT_1_PROBLEM = {
    Language.ENGLISH: "Project 1 problem",
    Language.SPANISH: "Problema del proyecto 1",
}
PROJECT_1_APPROACH = {
    Language.ENGLISH: "Project 1 approach",
    Language.SPANISH: "Enfoque del proyecto 1",
}
PROJECT_1_OUTCOME = {
    Language.ENGLISH: "Project 1 outcome",
    Language.SPANISH: "Resultado del proyecto 1",
}

PROJECT_2_TITLE = {
    Language.ENGLISH: "Project 2",
    Language.SPANISH: "Proyecto 2",
}
PROJECT_2_SLUG = "project-2"
PROJECT_2_SUMMARY = {
    Language.ENGLISH: "Project 2 summary",
    Language.SPANISH: "Resumen del proyecto 2",
}
PROJECT_2_PROBLEM = {
    Language.ENGLISH: "Project 2 problem",
    Language.SPANISH: "Problema del proyecto 2",
}

PROJECT_NON_FEATURED_TITLE = {
    Language.ENGLISH: "Project 3",
    Language.SPANISH: "Proyecto 3",
}
PROJECT_NON_FEATURED_SLUG = "project-3"
PROJECT_NON_FEATURED_SUMMARY = {
    Language.ENGLISH: "Project 3 summary",
    Language.SPANISH: "Resumen del proyecto 3",
}
PROJECT_NON_FEATURED_PROBLEM = {
    Language.ENGLISH: "Project 3 problem",
    Language.SPANISH: "Problema del proyecto 3",
}

# Services data
SERVICES_SECTION_TITLE = {
    Language.ENGLISH: "Services",
    Language.SPANISH: "Servicios",
}

SERVICE_1_TITLE = {
    Language.ENGLISH: "Service 1",
    Language.SPANISH: "Servicio 1",
}
SERVICE_1_SLUG = "service-1"
SERVICE_1_SHORT_DESCRIPTION = {
    Language.ENGLISH: "Service 1 description",
    Language.SPANISH: "Descripción del servicio 1",
}
SERVICE_1_LONG_DESCRIPTION = {
    Language.ENGLISH: "Service 1 long description",
    Language.SPANISH: "Descripción larga del servicio 1",
}

SERVICE_2_TITLE = {
    Language.ENGLISH: "Service 2",
    Language.SPANISH: "Servicio 2",
}
SERVICE_2_SLUG = "service-2"
SERVICE_2_SHORT_DESCRIPTION = {
    Language.ENGLISH: "Service 2 description",
    Language.SPANISH: "Descripción del servicio 2",
}
SERVICE_2_LONG_DESCRIPTION = {
    Language.ENGLISH: "Service 2 long description",
    Language.SPANISH: "Descripción larga del servicio 2",
}

SERVICE_INACTIVE_TITLE = {
    Language.ENGLISH: "Service 3",
    Language.SPANISH: "Servicio 3",
}
SERVICE_INACTIVE_SLUG = "service-3"
SERVICE_INACTIVE_SHORT_DESCRIPTION = {
    Language.ENGLISH: "Service 3 description",
    Language.SPANISH: "Descripción del servicio 3",
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
    Language.ENGLISH: "1 year, 2 months",
    Language.SPANISH: "1 año, 2 meses",
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
    Language.ENGLISH: "2 years, 3 months",
    Language.SPANISH: "2 años, 3 meses",
}

EXPECTED_NUMBER_OF_EXPERIENCES = 2

# Education data
EDUCATION_1_TITLE = {
    Language.ENGLISH: "Test education title 1",
    Language.SPANISH: "Título de educación de prueba 1",
}
EDUCATION_1_INSTITUTION = "Test University 1"
EDUCATION_1_LOCATION = {
    Language.ENGLISH: "Test City 1",
    Language.SPANISH: "Ciudad de prueba 1",
}
EDUCATION_1_DESCRIPTION = {
    Language.ENGLISH: "Test education description 1",
    Language.SPANISH: "Descripción de educación de prueba 1",
}
EDUCATION_1_START_DATE = date(2015, 9, 1)
EDUCATION_1_END_DATE = date(2019, 6, 30)
EDUCATION_1_PERIOD = {
    Language.ENGLISH: "Sep, 2015 - Jun, 2019",
    Language.SPANISH: "Sep, 2015 - Jun, 2019",
}
EDUCATION_1_DURATION = {
    Language.ENGLISH: "3 years, 9 months",
    Language.SPANISH: "3 años, 9 meses",
}

EDUCATION_2_TITLE = {
    Language.ENGLISH: "Test education title 2",
    Language.SPANISH: "Título de educación de prueba 2",
}
EDUCATION_2_INSTITUTION = "Test University 2"
EDUCATION_2_LOCATION = {
    Language.ENGLISH: "Test City 2",
    Language.SPANISH: "Ciudad de prueba 2",
}
EDUCATION_2_DESCRIPTION = {
    Language.ENGLISH: "Test education description 2",
    Language.SPANISH: "Descripción de educación de prueba 2",
}
EDUCATION_2_START_DATE = date(2019, 9, 1)
EDUCATION_2_END_DATE = date(2020, 6, 30)
EDUCATION_2_PERIOD = {
    Language.ENGLISH: "Sep, 2019 - Jun, 2020",
    Language.SPANISH: "Sep, 2019 - Jun, 2020",
}
EDUCATION_2_DURATION = {
    Language.ENGLISH: "9 months",
    Language.SPANISH: "9 meses",
}

EXPECTED_NUMBER_OF_EDUCATION_ENTRIES = 2

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

SOURCE_CODE_NOTE_TEXT = {
    Language.ENGLISH: "The source code of this website is available on GitHub under the MIT License.",
    Language.SPANISH: "El código fuente de este sitio web está disponible en GitHub bajo licencia MIT.",
}
SOURCE_CODE_GITHUB_LINK = "https://github.com/roberfi/personal-portfolio"

# Process steps data
PROCESS_STEPS_SECTION_TITLE = {
    Language.ENGLISH: "How I work",
    Language.SPANISH: "Cómo trabajo",
}

PROCESS_STEP_1_ICON_NAME = "chat"
PROCESS_STEP_1_TITLE = {
    Language.ENGLISH: "Discovery",
    Language.SPANISH: "Descubrimiento",
}
PROCESS_STEP_1_DESCRIPTION = {
    Language.ENGLISH: "We analyze your needs and define the project scope.",
    Language.SPANISH: "Analizamos tus necesidades y definimos el alcance del proyecto.",
}

PROCESS_STEP_2_ICON_NAME = "code"
PROCESS_STEP_2_TITLE = {
    Language.ENGLISH: "Development",
    Language.SPANISH: "Desarrollo",
}
PROCESS_STEP_2_DESCRIPTION = {
    Language.ENGLISH: "We build the solution iteratively, with continuous feedback.",
    Language.SPANISH: "Construimos la solución de forma iterativa, con feedback continuo.",
}

# Home CTA texts (default copy of the c-cta-block component)
HOME_CTA_EYEBROW = {
    Language.ENGLISH: "Ready to start?",
    Language.SPANISH: "¿Listo para empezar?",
}
HOME_CTA_TITLE = {
    Language.ENGLISH: "Do you have a project in mind?",
    Language.SPANISH: "¿Tienes un proyecto en mente?",
}
HOME_CTA_PRIMARY_TEXT = {
    Language.ENGLISH: "Let's talk",
    Language.SPANISH: "Hablemos",
}
