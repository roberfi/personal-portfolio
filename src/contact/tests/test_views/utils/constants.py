from __future__ import annotations

from datetime import datetime, timezone

from utils.test_utils.constants import Language

# Contact page ids
CONTACT_CONTAINER_ID = "contact"

CONTACT_TITLE_ID = "get-in-touch-title"

CONTACT_RESPONSE_ALERTS_ID = "response-alerts"

CONTACT_FORM_ID = "contact-form"
CONTACT_FORM_NAME_LABEL_ID = "contact-form-name-label"
CONTACT_FORM_EMAIL_LABEL_ID = "contact-form-email-label"
CONTACT_FORM_SUBJECT_LABEL_ID = "contact-form-subject-label"
CONTACT_FORM_MESSAGE_LABEL_ID = "contact-form-message-label"
CONTACT_FORM_SUBMIT_BUTTON_ID = "contact-form-submit-button"

# Form field ids (Django auto-generates these as id_<fieldname>)
CONTACT_FORM_NAME_ID = "id_name"
CONTACT_FORM_EMAIL_ID = "id_email"
CONTACT_FORM_SUBJECT_ID = "id_subject"
CONTACT_FORM_MESSAGE_ID = "id_message"

CONTACT_FORM_NAME_ERROR_ID = "contact-form-name-error"
CONTACT_FORM_EMAIL_ERROR_ID = "contact-form-email-error"
CONTACT_FORM_SUBJECT_ERROR_ID = "contact-form-subject-error"
CONTACT_FORM_MESSAGE_ERROR_ID = "contact-form-message-error"


CONTACT_ADDITIONAL_INFO_ID = "contact-additional-info"

# Test data
TEST_NAME = "Test Name"
TEST_EMAIL = "test@example.com"
TEST_SUBJECT = "Test Subject"
TEST_MESSAGE = "This is a test message with enough characters to pass validation."
TEST_SHORT_MESSAGE = "Short"  # Less than 10 characters
TEST_INVALID_EMAIL = "invalid-email"

TO_EMAIL_ADDRESS = "contact@localhost"
FROM_EMAIL_ADDRESS = "noreply@localhost"

EMAIL_BODY_TEMPLATE = "New contact message from {name}\n\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}\n"

# Mocked now datetime
MOCKED_NOW = datetime(2026, 1, 10, 12, 21, 43, 123456, tzinfo=timezone.utc)

MOCKED_ERROR_MESSAGE = "Test error message"

# Expected texts
CONTACT_PAGE_TITLE = {
    Language.ENGLISH: "Get in Touch",
    Language.SPANISH: "Contactar conmigo",
}

CONTACT_PAGE_DESCRIPTION = {
    Language.ENGLISH: (
        "Do you have a question or want to work together?"
        " Feel free to send me a message and I will respond as soon as possible."
    ),
    Language.SPANISH: (
        "¿Tienes alguna pregunta o quieres trabajar conmigo? Envíame un mensaje y te responderé lo antes posible."
    ),
}

SUCCESS_MESSAGE = {
    Language.ENGLISH: "Thank you for your message! I'll get back to you as soon as possible.",
    Language.SPANISH: "¡Gracias por tu mensaje! Te responderé lo antes posible.",
}

LABEL_NAME_TEXT = {
    Language.ENGLISH: "Name",
    Language.SPANISH: "Nombre",
}
LABEL_EMAIL_TEXT = {
    Language.ENGLISH: "Email",
    Language.SPANISH: "Correo electrónico",
}
LABEL_SUBJECT_TEXT = {
    Language.ENGLISH: "Subject",
    Language.SPANISH: "Asunto",
}
LABEL_MESSAGE_TEXT = {
    Language.ENGLISH: "Message",
    Language.SPANISH: "Mensaje",
}

INPUT_NAME_PLACEHOLDER = {
    Language.ENGLISH: "Your name",
    Language.SPANISH: "Tu nombre",
}
INPUT_EMAIL_PLACEHOLDER = {
    Language.ENGLISH: "your.email@example.com",
    Language.SPANISH: "tu.email@ejemplo.com",
}
INPUT_SUBJECT_PLACEHOLDER = {
    Language.ENGLISH: "Message subject",
    Language.SPANISH: "Asunto del mensaje",
}
INPUT_MESSAGE_PLACEHOLDER = {
    Language.ENGLISH: "Write your message here...",
    Language.SPANISH: "Escribe aquí tu mensaje...",
}

VALIDATION_ERROR_INVALID_EMAIL = {
    Language.ENGLISH: "Enter a valid email address.",
    Language.SPANISH: "Introduzca una dirección de correo electrónico válida.",
}
VALIDATION_ERROR_SHORT_MESSAGE = {
    Language.ENGLISH: "Message must be at least 10 characters long.",
    Language.SPANISH: "El mensaje debe tener al menos 10 caracteres.",
}

SUBMIT_BUTTON_TEXT = {
    Language.ENGLISH: "Send Message",
    Language.SPANISH: "Enviar Mensaje",
}

ADDITIONAL_INFO_TEXT = {
    Language.ENGLISH: "Your information is safe and will only be used to respond to your inquiry.",
    Language.SPANISH: "Tu información está segura y sólo se utilizará para responder a tu consulta.",
}

# Metadata constants
META_TITLE = {
    Language.ENGLISH: "Contact | Portfolio",
    Language.SPANISH: "Contacto | Portfolio",
}

META_DESCRIPTION = {
    Language.ENGLISH: "Get in touch with me. Send me a message and I'll respond as soon as possible.",
    Language.SPANISH: "Ponte en contacto conmigo. Envíame un mensaje y te responderé lo antes posible.",
}

# Base keywords from template (portfolio, CV, biography, career) + page-specific keywords
META_KEYWORDS = {
    Language.ENGLISH: "portfolio, CV, biography, career, contact, get in touch, message, email",
    Language.SPANISH: "portfolio, CV, biografía, carrera, contacto, contactar, mensaje, correo electrónico, email",
}
