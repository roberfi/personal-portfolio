/* global grecaptcha */

/**
 * Setup contact form with reCAPTCHA v3 integration
 * @param {string} siteKey - Google reCAPTCHA site key
 * @param {string} formId - Form element ID (default: 'contact-form')
 * @param {string} buttonId - Submit button element ID (default: 'contact-form-submit-button')
 */
export function setupContactForm(
  siteKey,
  formId = "contact-form",
  buttonId = "contact-form-submit-button",
) {
  const form = document.getElementById(formId);
  const submitButton = document.getElementById(buttonId);
  const loadingTemplate = document.getElementById(
    "submit-button-loading-template",
  );
  const errorTemplate = document.getElementById("recaptcha-error-template");
  const alertsContainer = document.getElementById("response-alerts");

  if (!form || !submitButton || !loadingTemplate || !errorTemplate) {
    console.error("Required elements not found for contact form setup");
    return;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const originalButtonContent = submitButton.innerHTML;
    submitButton.innerHTML = loadingTemplate.innerHTML;
    submitButton.disabled = true;

    grecaptcha.ready(function () {
      grecaptcha
        .execute(siteKey, { action: "contact_form" })
        .then(function (token) {
          // Add token to hidden input
          const recaptchaInput = document.getElementById("id_recaptcha_token");
          if (recaptchaInput) {
            recaptchaInput.value = token;
          }

          // Submit the form
          form.submit();
        })
        .catch(function (error) {
          console.error("reCAPTCHA error:", error);

          // Restore button state
          submitButton.innerHTML = originalButtonContent;
          submitButton.disabled = false;

          // Show error alert using template clone
          const alertClone = errorTemplate.content.cloneNode(true);
          alertsContainer.insertBefore(alertClone, alertsContainer.firstChild);
        });
    });
  });
}
