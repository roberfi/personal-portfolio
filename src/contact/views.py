from __future__ import annotations

import json
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

from utils.types import PageMetadata

from .forms import ContactForm

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from contact.models import ContactMessage


class ContactViewContext(TypedDict):
    """Context for the ContactView."""

    page_metadata: PageMetadata
    form: ContactForm
    recaptcha_site_key: str | None


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

        page_title = gettext("Contact") + " | Portfolio"
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
        )

    def __send_email_notification(self, contact_message: ContactMessage) -> None:
        """Send email notification about new contact message.

        It will also handle any exceptions during email sending,
        saving the error details to the contact message and logging the error.

        Args:
            contact_message: The ContactMessage instance containing the message details.
        """
        try:
            # Prepare email to site owner
            subject = f"[Portfolio Contact] {contact_message.subject}"
            message_body = (
                f"New contact message from {contact_message.name}\n\n"
                f"Email: {contact_message.email}\n"
                f"Subject: {contact_message.subject}\n\n"
                f"Message:\n{contact_message.message}\n"
            )

            email = EmailMessage(
                subject=subject,
                body=message_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=(settings.CONTACT_EMAIL,),
                reply_to=(contact_message.email,),
            )
            email.send(fail_silently=False)

        except Exception as e:
            # Save the error to the contact message for later review
            contact_message.error = traceback.format_exc()
            contact_message.save(update_fields=("error",))

            # Log the error
            # TODO: Replace with proper logging
            print(f"Error sending email: {e}")

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
            # TODO: Replace with proper logging
            print("reCAPTCHA token missing")
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
                print(f"reCAPTCHA verification passed; score: {score}")
                return RecaptchaResult(is_valid=True, score=score)

            # TODO: Replace with proper logging
            print(f"reCAPTCHA verification failed: {success=}, {score=}, {action=}")
            return RecaptchaResult(is_valid=False, score=score)

        except requests.RequestException as e:
            # Network or API error - allow submission to avoid blocking legitimate users
            # TODO: Replace with proper logging
            print(f"reCAPTCHA API error: {e}")
            return RecaptchaResult(is_valid=True, score=None)

        except Exception as e:
            # Unexpected error - log and reject for security
            # TODO: Replace with proper logging
            print(f"Unexpected reCAPTCHA error: {e}")
            return RecaptchaResult(is_valid=False, score=None)

    def get(self, request: HttpRequest) -> HttpResponse:
        """Deal with GET requests to the contact page.

        Display the contact form.

        Args:
            request: The HTTP request object.

        Returns:
            An HttpResponse with the rendered contact form.
        """
        form = ContactForm()
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

            self.__send_email_notification(contact_message)

            messages.success(
                request,
                gettext("Thank you for your message! I'll get back to you as soon as possible."),
            )
            return redirect("contact")

        return render(request, "contact.html", self.__get_view_context(form))
