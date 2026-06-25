from __future__ import annotations

from datetime import datetime, timezone

from utils.test_utils.constants import Language

# Contact page ids
CONTACT_CONTAINER_ID = "contact"

CONTACT_TITLE_ID = "contact-title"

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

CONTACT_FORM_SERVICE_INTEREST_LABEL_ID = "contact-form-service-interest-label"
CONTACT_FORM_BUDGET_RANGE_LABEL_ID = "contact-form-budget-range-label"
CONTACT_FORM_TIMELINE_LABEL_ID = "contact-form-timeline-label"

CONTACT_FORM_SERVICE_INTEREST_ID = "id_service_interest"
CONTACT_FORM_BUDGET_RANGE_ID = "id_budget_range"
CONTACT_FORM_TIMELINE_ID = "id_timeline"

CONTACT_FORM_PRIVACY_POLICY_ID = "contact-form-privacy-policy"
CONTACT_FORM_PRIVACY_POLICY_CHECKBOX_ID = "id_privacy_policy_accepted"
CONTACT_FORM_PRIVACY_POLICY_LINK_ID = "contact-form-privacy-policy-link"
CONTACT_FORM_PRIVACY_POLICY_ERROR_ID = "contact-form-privacy-policy-error"

# Test data
TEST_NAME = "Test Name"
TEST_EMAIL = "test@example.com"
TEST_SUBJECT = "Test Subject"
TEST_MESSAGE = "This is a test message with enough characters to pass validation."
TEST_SHORT_MESSAGE = "Short"  # Less than 10 characters
TEST_INVALID_EMAIL = "invalid-email"

TEST_SERVICE_SLUG = "test-service"
TEST_SERVICE_TITLE = "Test Service"
TEST_SERVICE_INACTIVE_SLUG = "inactive-service"
TEST_BUDGET_RANGE_VALUE = "1k_5k"
TEST_BUDGET_RANGE_DISPLAY = {
    Language.ENGLISH: "€1,000 \u2013 €5,000",
    Language.SPANISH: "1.000 € \u2013 5.000 €",
}
TEST_TIMELINE_VALUE = "1m_3m"
TEST_TIMELINE_DISPLAY = {
    Language.ENGLISH: "1 \u2013 3 months",
    Language.SPANISH: "1 \u2013 3 meses",
}

TO_EMAIL_ADDRESS = "contact@localhost"
FROM_EMAIL_ADDRESS = "noreply@localhost"

EMAIL_BODY_TEMPLATE = "New contact message from {name}\n\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}\n"
EMAIL_BODY_WITH_QUALIFICATION_TEMPLATE = (
    "New contact message from {name}\n\n"
    "Email: {email}\n"
    "Subject: {subject}\n\n"
    "Message:\n{message}\n"
    "\n{service_interest_label}: {service_interest}\n"
    "{budget_range_label}: {budget_range}\n"
    "{timeline_label}: {timeline}\n"
)

# Mocked now datetime
MOCKED_NOW = datetime(2026, 1, 10, 12, 21, 43, 123456, tzinfo=timezone.utc)

MOCKED_ERROR_MESSAGE = "Test error message"

# Expected texts
CONTACT_PAGE_TITLE = {
    Language.ENGLISH: "Contact",
    Language.SPANISH: "Contacto",
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
LABEL_SERVICE_INTEREST_TEXT = {
    Language.ENGLISH: "Service Interest",
    Language.SPANISH: "Servicio de interés",
}
LABEL_BUDGET_RANGE_TEXT = {
    Language.ENGLISH: "Budget Range",
    Language.SPANISH: "Presupuesto",
}
LABEL_TIMELINE_TEXT = {
    Language.ENGLISH: "Timeline",
    Language.SPANISH: "Plazo",
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

PRIVACY_POLICY_LABEL_TEXT = {
    Language.ENGLISH: "I accept the",
    Language.SPANISH: "Acepto la",
}

VALIDATION_ERROR_PRIVACY_POLICY_NOT_ACCEPTED = {
    Language.ENGLISH: "You must accept the privacy policy to send this message.",
    Language.SPANISH: "Debes aceptar la política de privacidad para enviar este mensaje.",
}

# Metadata constants
META_TITLE = {
    Language.ENGLISH: "Contact",
    Language.SPANISH: "Contacto",
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

# reCAPTCHA error messages
RECAPTCHA_VERIFICATION_FAILED = {
    Language.ENGLISH: (
        "reCAPTCHA verification failed. Please try again. If the problem persists, contact me directly."
    ),
    Language.SPANISH: (
        "La verificación de reCAPTCHA ha fallado. Por favor, inténtalo de nuevo. "
        "Si el problema persiste, contacta directamente."
    ),
}

CONTACT_FORM_CUSTOM_INTRO = {
    Language.ENGLISH: "Tell me briefly about your project. No commitment.",
    Language.SPANISH: "Cuéntame brevemente tu proyecto. Sin compromiso.",
}
