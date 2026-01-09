from __future__ import annotations

from types import MappingProxyType

from django import forms
from django.utils.translation import gettext_lazy

from contact.models import ContactMessage

MINIMUM_MESSAGE_LENGTH = 10

CONTACT_FORM_FIELD_NAME = "name"
CONTACT_FORM_FIELD_EMAIL = "email"
CONTACT_FORM_FIELD_SUBJECT = "subject"
CONTACT_FORM_FIELD_MESSAGE = "message"


class ContactForm(forms.ModelForm[ContactMessage]):
    """Contact form for visitors to send messages."""

    class Meta:
        model = ContactMessage
        fields = (
            CONTACT_FORM_FIELD_NAME,
            CONTACT_FORM_FIELD_EMAIL,
            CONTACT_FORM_FIELD_SUBJECT,
            CONTACT_FORM_FIELD_MESSAGE,
        )
        widgets = MappingProxyType(
            {
                CONTACT_FORM_FIELD_NAME: forms.TextInput(
                    attrs={
                        "class": (
                            "input input-bordered w-full focus:outline-none focus:border-primary/50"
                            " focus:ring-2 focus:ring-primary/20 transition-all duration-200"
                        ),
                        "placeholder": gettext_lazy("Your name"),
                    }
                ),
                CONTACT_FORM_FIELD_EMAIL: forms.EmailInput(
                    attrs={
                        "class": (
                            "input input-bordered w-full focus:outline-none focus:border-primary/50"
                            " focus:ring-2 focus:ring-primary/20 transition-all duration-200"
                        ),
                        "placeholder": gettext_lazy("your.email@example.com"),
                    }
                ),
                CONTACT_FORM_FIELD_SUBJECT: forms.TextInput(
                    attrs={
                        "class": (
                            "input input-bordered w-full focus:outline-none focus:border-primary/50"
                            " focus:ring-2 focus:ring-primary/20 transition-all duration-200"
                        ),
                        "placeholder": gettext_lazy("Message subject"),
                    }
                ),
                CONTACT_FORM_FIELD_MESSAGE: forms.Textarea(
                    attrs={
                        "class": (
                            "textarea textarea-bordered w-full h-32 focus:outline-none focus:border-primary/50"
                            " focus:ring-2 focus:ring-primary/20 transition-all duration-200"
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
