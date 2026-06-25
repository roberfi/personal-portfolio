from __future__ import annotations

from types import MappingProxyType
from typing import Any

from django import forms
from django.utils.translation import gettext_lazy

from contact.models import BudgetRange, ContactFormConfiguration, ContactMessage, EmailProvider, Timeline
from home.models import Service

MINIMUM_MESSAGE_LENGTH = 10

_SELECT_CSS = (
    "select select-bordered w-full bg-base-200 focus:outline-none focus:border-primary/50"
    " focus:ring-2 focus:ring-primary/20 transition-all duration-200"
)

CONTACT_FORM_FIELD_NAME = "name"
CONTACT_FORM_FIELD_EMAIL = "email"
CONTACT_FORM_FIELD_SUBJECT = "subject"
CONTACT_FORM_FIELD_SERVICE_INTEREST = "service_interest"
CONTACT_FORM_FIELD_BUDGET_RANGE = "budget_range"
CONTACT_FORM_FIELD_TIMELINE = "timeline"
CONTACT_FORM_FIELD_MESSAGE = "message"
CONTACT_FORM_FIELD_RECAPTCHA = "recaptcha_token"
CONTACT_FORM_FIELD_PRIVACY_POLICY_ACCEPTED = "privacy_policy_accepted"


class ContactForm(forms.ModelForm[ContactMessage]):
    """Contact form for visitors to send messages."""

    recaptcha_token = forms.CharField(widget=forms.HiddenInput(), required=False)
    privacy_policy_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}),
        error_messages={"required": gettext_lazy("You must accept the privacy policy to send this message.")},
    )
    service_interest: forms.ModelChoiceField[Service] = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        required=False,
        empty_label=gettext_lazy("No specific service"),
        widget=forms.Select(attrs={"class": _SELECT_CSS}),
        label=gettext_lazy("Service Interest"),
    )
    budget_range = forms.ChoiceField(
        choices=[("", gettext_lazy("Not specified")), *BudgetRange.choices],
        required=False,
        widget=forms.Select(attrs={"class": _SELECT_CSS}),
        label=gettext_lazy("Budget Range"),
    )
    timeline = forms.ChoiceField(
        choices=[("", gettext_lazy("Not specified")), *Timeline.choices],
        required=False,
        widget=forms.Select(attrs={"class": _SELECT_CSS}),
        label=gettext_lazy("Timeline"),
    )

    class Meta:
        model = ContactMessage
        fields = (
            CONTACT_FORM_FIELD_NAME,
            CONTACT_FORM_FIELD_EMAIL,
            CONTACT_FORM_FIELD_SUBJECT,
            CONTACT_FORM_FIELD_SERVICE_INTEREST,
            CONTACT_FORM_FIELD_BUDGET_RANGE,
            CONTACT_FORM_FIELD_TIMELINE,
            CONTACT_FORM_FIELD_MESSAGE,
        )
        widgets = MappingProxyType(
            {
                CONTACT_FORM_FIELD_NAME: forms.TextInput(
                    attrs={
                        "class": (
                            "input input-bordered w-full bg-base-300/40 focus:outline-none focus:border-primary/50"
                            " focus:ring-2 focus:ring-primary/20 transition-all duration-200"
                        ),
                        "placeholder": gettext_lazy("Your name"),
                    }
                ),
                CONTACT_FORM_FIELD_EMAIL: forms.EmailInput(
                    attrs={
                        "class": (
                            "input input-bordered w-full bg-base-300/40 focus:outline-none focus:border-primary/50"
                            " focus:ring-2 focus:ring-primary/20 transition-all duration-200"
                        ),
                        "placeholder": gettext_lazy("your.email@example.com"),
                    }
                ),
                CONTACT_FORM_FIELD_SUBJECT: forms.TextInput(
                    attrs={
                        "class": (
                            "input input-bordered w-full bg-base-300/40 focus:outline-none focus:border-primary/50"
                            " focus:ring-2 focus:ring-primary/20 transition-all duration-200"
                        ),
                        "placeholder": gettext_lazy("Message subject"),
                    }
                ),
                CONTACT_FORM_FIELD_MESSAGE: forms.Textarea(
                    attrs={
                        "class": (
                            "textarea textarea-bordered w-full h-32 bg-base-300/40 focus:outline-none"
                            " focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-all duration-200"
                        ),
                        "placeholder": gettext_lazy("Write your message here..."),
                        "rows": 6,
                    }
                ),
            }
        )
        labels = MappingProxyType(
            {
                CONTACT_FORM_FIELD_NAME: gettext_lazy("Name"),
                CONTACT_FORM_FIELD_EMAIL: gettext_lazy("Email"),
                CONTACT_FORM_FIELD_SUBJECT: gettext_lazy("Subject"),
                CONTACT_FORM_FIELD_MESSAGE: gettext_lazy("Message"),
            }
        )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        if not ContactFormConfiguration.get_solo().legal_and_privacy:
            del self.fields[CONTACT_FORM_FIELD_PRIVACY_POLICY_ACCEPTED]

    def clean_message(self) -> str:
        """Validate message length."""
        message = self.cleaned_data.get("message", "")

        if not isinstance(message, str):
            raise forms.ValidationError(gettext_lazy("Invalid message."))

        if len(message) < MINIMUM_MESSAGE_LENGTH:
            raise forms.ValidationError(
                gettext_lazy("Message must be at least %(min_length)d characters long.")
                % {"min_length": MINIMUM_MESSAGE_LENGTH}
            )

        return message


class ContactFormConfigurationForm(forms.ModelForm[ContactFormConfiguration]):
    """Admin form for ContactFormConfiguration, with provider-specific settings."""

    smtp_host = forms.CharField(label=gettext_lazy("Host"), required=False)
    smtp_port = forms.IntegerField(label=gettext_lazy("Port"), required=False, initial=587)
    smtp_use_tls = forms.BooleanField(label=gettext_lazy("Use TLS"), required=False, initial=True)
    smtp_use_ssl = forms.BooleanField(label=gettext_lazy("Use SSL"), required=False)
    smtp_username = forms.CharField(label=gettext_lazy("Username"), required=False)
    smtp_password = forms.CharField(
        label=gettext_lazy("Password"), required=False, widget=forms.PasswordInput(render_value=True)
    )
    smtp_timeout = forms.IntegerField(label=gettext_lazy("Timeout (seconds)"), required=False, initial=10)
    brevo_api_key = forms.CharField(
        label=gettext_lazy("API key"), required=False, widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = ContactFormConfiguration
        fields = ("email_provider", "default_from_email", "contact_email", "legal_and_privacy")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        provider_config = self.instance.provider_config
        self.fields["smtp_host"].initial = provider_config.get("host", "")
        self.fields["smtp_port"].initial = provider_config.get("port", 587)
        self.fields["smtp_use_tls"].initial = provider_config.get("use_tls", True)
        self.fields["smtp_use_ssl"].initial = provider_config.get("use_ssl", False)
        self.fields["smtp_username"].initial = provider_config.get("username", "")
        self.fields["smtp_password"].initial = provider_config.get("password", "")
        self.fields["smtp_timeout"].initial = provider_config.get("timeout", 10)
        self.fields["brevo_api_key"].initial = provider_config.get("api_key", "")

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean() or {}

        if cleaned_data.get("email_provider") == EmailProvider.SMTP and not cleaned_data.get("smtp_host"):
            self.add_error("smtp_host", gettext_lazy("This field is required when using SMTP."))

        if cleaned_data.get("email_provider") == EmailProvider.BREVO_API and not cleaned_data.get("brevo_api_key"):
            self.add_error("brevo_api_key", gettext_lazy("This field is required when using the Brevo API."))

        return cleaned_data

    def save(self, commit: bool = True) -> ContactFormConfiguration:
        if self.cleaned_data.get("email_provider") == EmailProvider.BREVO_API:
            self.instance.provider_config = {"api_key": self.cleaned_data.get("brevo_api_key", "")}
        else:
            self.instance.provider_config = {
                "host": self.cleaned_data.get("smtp_host", ""),
                "port": self.cleaned_data.get("smtp_port") or 587,
                "use_tls": self.cleaned_data.get("smtp_use_tls", True),
                "use_ssl": self.cleaned_data.get("smtp_use_ssl", False),
                "username": self.cleaned_data.get("smtp_username", ""),
                "password": self.cleaned_data.get("smtp_password", ""),
                "timeout": self.cleaned_data.get("smtp_timeout") or 10,
            }

        return super().save(commit=commit)
