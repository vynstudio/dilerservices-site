const d = document, b = d.body;
// sticky header
const sticky = d.querySelector(".sticky-header"), main = d.querySelector(".header-style-one");
const onScroll = () => { const y = scrollY; sticky?.classList.toggle("fixed-header", y > 100); main?.classList.toggle("fixed-header", y > 1); };
addEventListener("scroll", onScroll, { passive: true }); onScroll();
// mobile menu
const setMenu = (open) => { b.classList.toggle("mobile-menu-visible", open); d.querySelectorAll(".mobile-nav-toggler").forEach((x) => x.setAttribute("aria-expanded", open)); };
d.querySelectorAll(".mobile-nav-toggler").forEach((x) => x.addEventListener("click", () => setMenu(true)));
d.querySelectorAll(".mobile-menu .close-btn, .mobile-menu .menu-backdrop, .mobile-menu .navigation a").forEach((x) => x.addEventListener("click", () => setMenu(false)));
d.addEventListener("keydown", (e) => e.key === "Escape" && setMenu(false));
// tabs
d.querySelectorAll("[data-tab]").forEach((a) => a.addEventListener("click", (e) => {
  e.preventDefault();
  const list = a.closest("ul"), pane = d.querySelector(a.dataset.tab);
  list.querySelectorAll("[data-tab]").forEach((x) => { x.classList.remove("active"); x.setAttribute("aria-selected", "false"); });
  a.classList.add("active"); a.setAttribute("aria-selected", "true");
  pane.parentElement.querySelectorAll(":scope > .tab-pane").forEach((p) => p.classList.remove("show", "active"));
  pane.classList.add("active"); requestAnimationFrame(() => pane.classList.add("show"));
  pane.querySelectorAll(".reveal").forEach((r) => r.classList.add("in"));
}));
// accordion
d.querySelectorAll(".accordion-box .acc-btn").forEach((btn) => btn.addEventListener("click", () => {
  const li = btn.closest(".accordion"), box = li.parentElement, open = !btn.classList.contains("active");
  box.querySelectorAll(".accordion").forEach((x) => {
    x.classList.remove("active-block"); x.querySelector(".acc-btn").classList.remove("active");
    x.querySelector(".acc-btn").setAttribute("aria-expanded", "false"); x.querySelector(".acc-content").classList.remove("current");
  });
  if (open) { li.classList.add("active-block"); btn.classList.add("active"); btn.setAttribute("aria-expanded", "true"); li.querySelector(".acc-content").classList.add("current"); }
}));
// reveal
const items = d.querySelectorAll(".reveal");
if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) items.forEach((x) => x.classList.add("in"));
else {
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
  items.forEach((x) => io.observe(x));
}
d.documentElement.classList.add("js");
