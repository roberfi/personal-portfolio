from __future__ import annotations

import json
import logging
import traceback
from typing import TYPE_CHECKING, Any, NamedTuple, TypedDict

import requests
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, gettext
from django.views import View

from home.models import PersonalInfo, Service
from utils.types import PageMetadata

from .forms import ContactForm
from .models import ContactFormConfiguration

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from contact.models import ContactMessage

contact_logger = logging.getLogger("contact")
recaptcha_logger = logging.getLogger("recaptcha")
security_logger = logging.getLogger("security")


class ContactViewContext(TypedDict):
    """Context for the ContactView."""

    page_metadata: PageMetadata
    form: ContactForm
    recaptcha_site_key: str | None
    privacy_notice: ContactFormConfiguration


class RecaptchaResult(NamedTuple):
    """Result of reCAPTCHA verification."""

    is_valid: bool
    score: float | None


class ContactView(View):
    """View to handle contact form submissions."""

    def __get_page_metadata(self) -> PageMetadata:
        """Get page metadata for SEO purposes.

        Returns:
            A PageMetadata dictionary with the metadata for the contact page.
        """

        name = PersonalInfo.objects.values_list("name", flat=True).first()
        suffix = f" | {name}" if name else ""
        page_title = gettext("Contact") + suffix
        page_description = gettext("Get in touch with me. Send me a message and I'll respond as soon as possible.")
        page_keywords = gettext("contact, get in touch, message, email")

        # JSON-LD structured data
        json_ld: dict[str, Any] = {
            "@context": {
                "@vocab": "https://schema.org/",
                "@language": get_language(),
            },
            "@type": "ContactPage",
            "name": page_title,
            "description": page_description,
        }

        return PageMetadata(
            page_title=page_title,
            page_description=page_description,
            page_keywords=page_keywords,
            json_ld=mark_safe(json.dumps(json_ld, ensure_ascii=False)),
        )

    def __get_view_context(self, form: ContactForm) -> ContactViewContext:
        """Get context for the contact template.

        Args:
            form: The contact form instance.

        Returns:
            A ContactViewContext dictionary with the context data for the contact template.
        """

        return ContactViewContext(
            form=form,
            page_metadata=self.__get_page_metadata(),
            recaptcha_site_key=settings.RECAPTCHA_SITE_KEY if settings.IS_RECAPTCHA_CONFIGURED else None,
            privacy_notice=ContactFormConfiguration.get_solo(),
        )

    def __send_email_notification(self, contact_message: ContactMessage) -> None:
        """Send email notification about new contact message.

        It will also handle any exceptions during email sending,
        saving the error details to the contact message and logging the error.

        Args:
            contact_message: The ContactMessage instance containing the message details.
        """
        try:
            config = ContactFormConfiguration.get_solo()

            # Prepare email to site owner
            subject = f"[Portfolio Contact] {contact_message.subject}"
            message_body = (
                f"New contact message from {contact_message.name}\n\n"
                f"Email: {contact_message.email}\n"
                f"Subject: {contact_message.subject}\n\n"
                f"Message:\n{contact_message.message}\n"
            )

            qualification_lines = []
            if contact_message.service_interest:
                qualification_lines.append(f"{gettext('Service Interest')}: {contact_message.service_interest.title}")
            if contact_message.budget_range:
                qualification_lines.append(f"{gettext('Budget Range')}: {contact_message.get_budget_range_display()}")
            if contact_message.timeline:
                qualification_lines.append(f"{gettext('Timeline')}: {contact_message.get_timeline_display()}")
            if qualification_lines:
                message_body += "\n" + "\n".join(qualification_lines) + "\n"

            email = EmailMessage(
                subject=subject,
                body=message_body,
                from_email=config.default_from_email,
                to=(config.contact_email,),
                reply_to=(contact_message.email,),
            )
            email.send(fail_silently=False)

        except Exception:
            # Save the error to the contact message for later review
            contact_message.error = traceback.format_exc()
            contact_message.save(update_fields=("error",))

            contact_logger.exception(
                "Failed to send email notification for contact message",
                extra={"contact_message_id": contact_message.pk},
            )

    def __verify_recaptcha(self, token: str) -> RecaptchaResult:
        """Verify reCAPTCHA v3 token with Google's API.

        Args:
            token: The reCAPTCHA token from the frontend.

        Returns:
            A RecaptchaResult named tuple with is_valid and score.
        """
        # If reCAPTCHA is not configured, allow the submission (development mode)
        if not settings.IS_RECAPTCHA_CONFIGURED:
            return RecaptchaResult(is_valid=True, score=None)

        # If reCAPTCHA is configured but no token provided, reject (spam attempt)
        if not token:
            security_logger.warning("reCAPTCHA token missing from contact form submission")
            return RecaptchaResult(is_valid=False, score=None)
        try:
            response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": settings.RECAPTCHA_SECRET_KEY,
                    "response": token,
                },
                timeout=5,
            )

            response.raise_for_status()

            result = response.json()

            success = result.get("success", False)
            score = result.get("score", 0.0)
            action = result.get("action", "")

            # Verify score meets threshold
            if success and action == "contact_form" and score >= settings.RECAPTCHA_SCORE_THRESHOLD:
                recaptcha_logger.info("reCAPTCHA verification passed", extra={"score": score})
                return RecaptchaResult(is_valid=True, score=score)

            security_logger.warning(
                "reCAPTCHA verification failed",
                extra={"success": success, "score": score, "action": action},
            )
            return RecaptchaResult(is_valid=False, score=score)

        except requests.RequestException:
            # Network or API error - allow submission to avoid blocking legitimate users
            recaptcha_logger.warning("reCAPTCHA API error, allowing submission", exc_info=True)
            return RecaptchaResult(is_valid=True, score=None)

        except Exception:
            # Unexpected error - log and reject for security
            recaptcha_logger.exception("Unexpected error during reCAPTCHA verification")
            return RecaptchaResult(is_valid=False, score=None)

    def get(self, request: HttpRequest) -> HttpResponse:
        """Deal with GET requests to the contact page.

        Display the contact form.

        Args:
            request: The HTTP request object.

        Returns:
            An HttpResponse with the rendered contact form.
        """
        initial: dict[str, Any] = {}
        service_slug = request.GET.get("service")
        if service_slug:
            service = Service.objects.filter(slug=service_slug, is_active=True).first()
            if service:
                initial["service_interest"] = service
        form = ContactForm(initial=initial)
        return render(request, "contact.html", self.__get_view_context(form))

    def post(self, request: HttpRequest) -> HttpResponse:
        """Deal with POST requests to the contact page.

        Process the contact form submission.

        Args:
            request: The HTTP request object.

        Returns:
            An HttpResponse redirecting on success or rendering the form with errors.
        """
        form = ContactForm(request.POST)

        if form.is_valid():
            # Verify reCAPTCHA
            recaptcha_token = form.cleaned_data.get("recaptcha_token", "")
            recaptcha_result = self.__verify_recaptcha(recaptcha_token)

            if not recaptcha_result.is_valid:
                messages.error(
                    request,
                    gettext(
                        "reCAPTCHA verification failed. Please try again. If the problem persists, contact me directly."
                    ),
                )
                return render(request, "contact.html", self.__get_view_context(form))

            contact_message = form.save(commit=False)
            contact_message.recaptcha_score = recaptcha_result.score
            contact_message.save()

            contact_logger.info(
                "Contact form submission received",
                extra={"contact_message_id": contact_message.pk, "recaptcha_score": recaptcha_result.score},
            )

            self.__send_email_notification(contact_message)

            messages.success(
                request,
                gettext("Thank you for your message! I'll get back to you as soon as possible."),
            )
            return redirect("contact")

        return render(request, "contact.html", self.__get_view_context(form))
