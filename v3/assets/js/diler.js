/* Diler Services: Web3Forms submission, order summary, FAQ search and keyboard support for the template's
   menu buttons. Runs after the template's main.js. */
(function ($) {
  'use strict';
  function money(n) { return '$' + (Math.round(n * 100) / 100).toFixed(n % 1 ? 2 : 0); }

  // Keyboard: the template's menu toggles are plain divs; make Enter and Space work like a click.
  document.querySelectorAll('.mobile-nav-icon, .menu-close').forEach(function (el) {
    el.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); el.click(); }
    });
  });

  // Slider arrows: name the template's owl buttons and keep them in the tab order.
  var isEs = document.documentElement.lang === 'es';
  var nameArrows = function () {
    document.querySelectorAll('.owl-prev, .owl-next').forEach(function (b) {
      b.removeAttribute('role');
      b.setAttribute('aria-label', b.classList.contains('owl-prev') ? (isEs ? 'Anterior' : 'Previous') : (isEs ? 'Siguiente' : 'Next'));
    });
  };
  if ($) { $(function () { setTimeout(nameArrows, 0); }); $(window).on('load', nameArrows); }

  // Give the template's custom selects an accessible name from their label.
  if ($ && $.fn) {
    $('select').each(function () {
      var id = this.id, lab = id ? document.querySelector('label[for="' + id + '"]') : null;
      var ns = $(this).next('.nice-select');
      if (lab && ns.length) { ns.attr({ role: 'button', 'aria-haspopup': 'listbox', 'aria-label': lab.textContent.replace(/\s*\*$/, '') }); }
    });
  }

  // Order summary (template checkout layout)
  var form = document.querySelector('.ds-order-form');
  if (form) {
    var area = document.querySelector('.checkout-tax-area');
    var cost = area ? area.getAttribute('data-at-cost') : 'at cost';
    var out = function (k) { return area.querySelector('[data-f="' + k + '"]'); };
    var svc = form.querySelector('select[name="Service"]');
    var ra = form.querySelector('select[name="Registered agent"]');
    var ein = form.querySelector('select[name="Add EIN filing"]');
    var want = new URLSearchParams(location.search).get('service');
    if (want && svc) {
      var opt = svc.querySelector('option[data-slug="' + want + '"]');
      if (opt) { svc.value = opt.value; }
      if (want === 'registered-agent' && ra) { ra.value = 'Monthly'; }
      if ($ && $.fn.niceSelect) { $(svc).niceSelect('update'); if (ra) { $(ra).niceSelect('update'); } }
    }
    var update = function () {
      var o = svc.options[svc.selectedIndex];
      var slug = o.getAttribute('data-slug');
      var fee = +o.getAttribute('data-fee');
      var st = o.getAttribute('data-state');
      var einOk = !(slug === 'formation-bundle' || slug === 'ein-filing' || slug === 'registered-agent');
      if (ein) { ein.disabled = !einOk; if (!einOk) { ein.value = 'No'; } if ($ && $.fn.niceSelect) { $(ein).niceSelect('update'); } }
      var einFee = ein && einOk ? +ein.options[ein.selectedIndex].getAttribute('data-fee') : 0;
      var raFee = ra ? +ra.options[ra.selectedIndex].getAttribute('data-fee') : 0;
      var unknown = st === '';
      var total = fee + einFee + raFee + (unknown ? 0 : +st);
      out('fee').textContent = money(fee + einFee);
      out('state').textContent = unknown ? cost : money(+st);
      out('ra').textContent = raFee ? money(raFee) : '—';
      var t = money(total) + (unknown ? ' + ' + cost : '');
      out('sum').textContent = t;
      var hidden = form.querySelector('[data-f="total"]');
      if (hidden) { hidden.value = t; }
    };
    [svc, ra, ein].forEach(function (s) { if (s) { s.addEventListener('change', update); } });
    if ($) { $(form).on('change', 'select', update); }
    update();
  }

  // FAQ search: faq.html?q=term shows the matching questions and opens the first one.
  var term = new URLSearchParams(location.search).get('q');
  if (term && document.querySelector('.faq-pricing-plan .accordion-item')) {
    var t = term.toLowerCase(), first = null;
    document.querySelectorAll('.faq-pricing-plan .accordion-item').forEach(function (it) {
      var hit = it.textContent.toLowerCase().indexOf(t) > -1;
      it.style.display = hit ? '' : 'none';
      if (hit && !first) { first = it; }
    });
    if (first) {
      var b = first.querySelector('.accordion-button');
      if (b && b.classList.contains('collapsed')) { b.click(); }
      first.scrollIntoView({ block: 'center' });
    }
  }

  // Send forms to Web3Forms without leaving the page.
  document.querySelectorAll('form.ds-form').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var btn = f.querySelector('button[type="submit"]');
      var msg = f.querySelector('.ds-form-msg') || (f.parentNode && f.parentNode.querySelector('.ds-form-msg'));
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = btn.getAttribute('data-sending') || label; }
      var data = new FormData(f);
      document.querySelectorAll('[form="' + f.id + '"]').forEach(function (x) { if (f.id && x.checked) { data.append(x.name, x.value); } });
      fetch(f.action, { method: 'POST', headers: { Accept: 'application/json' }, body: data })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.success) { throw new Error('fail'); }
          if (msg) { msg.classList.remove('ds-err'); msg.textContent = msg.getAttribute('data-ok'); }
          f.reset();
        })
        .catch(function () { if (msg) { msg.classList.add('ds-err'); msg.textContent = msg.getAttribute('data-err'); } })
        .then(function () { if (btn) { btn.disabled = false; btn.textContent = label; } });
    });
  });
})(window.jQuery);
