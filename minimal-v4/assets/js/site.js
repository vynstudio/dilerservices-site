(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var header = document.querySelector(".site-header");
  var menu = document.querySelector(".menu");

  function onScroll() {
    if (header) header.classList.toggle("is-stuck", window.scrollY > 8);
    if (reduce) return;
    document.querySelectorAll("[data-parallax]").forEach(function (img) {
      var frame = img.closest(".frame, .close-photo");
      if (!frame) return;
      var rect = frame.getBoundingClientRect();
      var view = window.innerHeight || 1;
      var progress = (rect.top + rect.height / 2 - view / 2) / view;
      var shift = Math.max(-18, Math.min(18, progress * -22));
      img.style.transform = "scale(1.08) translate3d(0, " + shift.toFixed(2) + "px, 0)";
    });
  }

  if (!reduce && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-in"); });
  }

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (menu) {
    menu.addEventListener("toggle", function () {
      document.documentElement.style.overflow = menu.open ? "hidden" : "";
    });
  }

  var form = document.querySelector("[data-contact]");
  if (!form) return;

  var select = form.querySelector("[name='service']");
  var requested = new URLSearchParams(location.search).get("service");
  if (select && requested) {
    Array.prototype.forEach.call(select.options, function (option) {
      if (option.value === requested) select.value = requested;
    });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var status = form.querySelector("[data-status]");
    var valid = true;
    form.querySelectorAll("[required]").forEach(function (field) {
      var error = field.parentElement.querySelector(".error");
      var missing = !field.value.trim();
      var badEmail = field.type === "email" && !missing && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value.trim());
      if (error) error.textContent = missing || badEmail ? field.dataset.error : "";
      field.setAttribute("aria-invalid", missing || badEmail ? "true" : "false");
      if (missing || badEmail) valid = false;
    });
    var trap = form.querySelector("[name='company']");
    if (trap && trap.value) {
      if (status) status.textContent = "";
      return;
    }
    if (!valid) {
      if (status) status.textContent = "";
      var first = form.querySelector("[aria-invalid='true']");
      if (first) first.focus();
      return;
    }
    var data = new FormData(form);
    var subject = "Diler Services inquiry";
    var service = data.get("service");
    if (service) subject += " — " + service;
    var body = [
      "Name: " + data.get("name"),
      "Email: " + data.get("email"),
      "Service: " + (service || ""),
      "",
      data.get("message")
    ].join("\n");
    window.location.href = "mailto:info@dilerservices.com?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    if (status) status.textContent = form.dataset.sent;
  });
})();
