(function () {
  /* TODO: replace with the Google Calendar appointment page URL. */
  var BOOK_CALL_URL = "TODO";

  /* TODO: point Start an LLC at the LLC service page once it exists. */
  var START_LLC_URL = "#start";

  var toggle = document.querySelector("[data-nav-toggle]");
  var panel = document.querySelector("[data-nav-panel]");

  function setOpen(open) {
    if (!panel || !toggle) return;
    panel.hidden = !open;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("nav-open", open);
  }

  if (toggle && panel) {
    setOpen(false);
    toggle.addEventListener("click", function () {
      setOpen(panel.hidden);
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setOpen(false);
      });
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setOpen(false);
    });
  }

  document.querySelectorAll("[data-book-call]").forEach(function (link) {
    if (BOOK_CALL_URL.indexOf("http") === 0) {
      link.setAttribute("href", BOOK_CALL_URL);
    }
  });

  document.querySelectorAll("[data-start-llc]").forEach(function (link) {
    if (START_LLC_URL) link.setAttribute("href", START_LLC_URL);
  });
})();
