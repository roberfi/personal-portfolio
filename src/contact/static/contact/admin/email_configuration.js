"use strict";

(function () {
  function toggleProviderFieldsets() {
    var select = document.getElementById("id_email_provider");

    if (!select) {
      return;
    }

    var provider = select.value;
    var fieldsets = document.querySelectorAll("[class*='email-config-']");

    fieldsets.forEach(function (fieldset) {
      var isMatch = fieldset.classList.contains("email-config-" + provider);
      fieldset.style.display = isMatch ? "" : "none";
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var select = document.getElementById("id_email_provider");

    if (!select) {
      return;
    }

    toggleProviderFieldsets();
    select.addEventListener("change", toggleProviderFieldsets);
  });
})();
