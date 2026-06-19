(function () {
  function init(container) {
    var sel = container.querySelector("select");
    var svg = container.querySelector("[data-icon-preview]");
    if (!sel || !svg) return;
    var defaultPath = svg.dataset.defaultPath;
    var pathEl = svg.querySelector("path");
    sel.addEventListener("change", function () {
      pathEl.setAttribute(
        "d",
        sel.options[sel.selectedIndex].dataset.path || defaultPath,
      );
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".icon-select-widget").forEach(init);
  });
})();
