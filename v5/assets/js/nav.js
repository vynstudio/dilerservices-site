(function () {
  /* TODO: replace with the Google Calendar appointment page URL. */
  var BOOK_CALL_URL = "TODO";

  /* TODO: point Start an LLC at the LLC service page once it exists. */
  var START_LLC_URL = "#start";

  var toggle = document.querySelector("[data-nav-toggle]");
  var panel = document.querySelector("[data-nav-panel]");
  var langRoots = document.querySelectorAll("[data-lang]");

  function setNav(open) {
    if (!panel || !toggle) return;
    panel.hidden = !open;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("nav-open", open);
  }

  function closeLang() {
    langRoots.forEach(function (root) {
      var button = root.querySelector("[data-lang-toggle]");
      var list = root.querySelector("[data-lang-list]");
      if (list) list.hidden = true;
      if (button) button.setAttribute("aria-expanded", "false");
    });
  }

  if (toggle && panel) {
    setNav(false);
    toggle.addEventListener("click", function () {
      var open = panel.hidden;
      closeLang();
      setNav(open);
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setNav(false);
      });
    });
  }

  langRoots.forEach(function (root) {
    var button = root.querySelector("[data-lang-toggle]");
    var list = root.querySelector("[data-lang-list]");
    if (!button || !list) return;
    button.addEventListener("click", function (event) {
      event.stopPropagation();
      var open = list.hidden;
      closeLang();
      list.hidden = !open;
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  document.addEventListener("click", function () {
    closeLang();
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeLang();
      setNav(false);
    }
  });

  document.querySelectorAll("[data-book-call]").forEach(function (link) {
    if (BOOK_CALL_URL.indexOf("http") === 0) {
      link.setAttribute("href", BOOK_CALL_URL);
    }
  });

  document.querySelectorAll("[data-start-llc]").forEach(function (link) {
    if (START_LLC_URL) link.setAttribute("href", START_LLC_URL);
  });
})();
