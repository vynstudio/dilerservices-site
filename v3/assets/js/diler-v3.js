/* Diler Services v3 proposal: form submission and the order summary. */
(function () {
  'use strict';
  function money(n) { return '$' + (Math.round(n * 100) / 100).toFixed(n % 1 ? 2 : 0); }

  // Order summary
  var form = document.querySelector('.ds-order-form');
  if (form) {
    var rows = document.querySelector('[data-f="rows"]');
    var sum = document.querySelector('[data-f="sum"]');
    var totalField = form.querySelector('[data-f="total"]');
    var atCost = document.querySelector('[data-at-cost]');
    var ein = form.querySelector('[data-ein]');
    var params = new URLSearchParams(location.search);
    var want = params.get('service');
    if (want) {
      if (want === 'registered-agent') {
        var m = form.querySelector('input[name="Registered agent"][value="Monthly"]'); if (m) m.checked = true;
      } else {
        var r = form.querySelector('input[name="Service"][data-slug="' + want + '"]'); if (r) r.checked = true;
      }
    }
    var cost = atCost ? atCost.getAttribute('data-at-cost') : 'at cost';
    var update = function () {
      var svc = form.querySelector('input[name="Service"]:checked');
      var ra = form.querySelector('input[name="Registered agent"]:checked');
      var items = [];
      if (svc) items.push([svc.dataset.label, +svc.dataset.fee, svc.dataset.state === '' ? null : +svc.dataset.state]);
      var bundle = svc && svc.dataset.slug === 'formation-bundle';
      if (ein) { ein.disabled = bundle || (svc && svc.dataset.slug === 'ein-filing'); if (ein.disabled) ein.checked = false; }
      if (ein && ein.checked) items.push([ein.parentNode.textContent.trim(), 95, 0]);
      if (ra && +ra.dataset.fee > 0) items.push([ra.dataset.label, +ra.dataset.fee, 0]);
      var total = 0, unknownState = false;
      rows.innerHTML = '';
      items.forEach(function (it) {
        total += it[1] + (it[2] || 0);
        if (it[2] === null) unknownState = true;
        var tr = document.createElement('tr');
        tr.innerHTML = '<td></td><td></td><td></td>';
        tr.children[0].textContent = it[0];
        tr.children[1].textContent = money(it[1]);
        tr.children[2].textContent = it[2] === null ? cost : it[2] ? money(it[2]) : '—';
        rows.appendChild(tr);
      });
      var text = money(total) + (unknownState ? ' + ' + cost : '');
      sum.textContent = text;
      if (totalField) totalField.value = text;
    };
    form.addEventListener('change', update);
    update();
  }

  // Submit forms to Web3Forms without leaving the page
  document.querySelectorAll('form.ds-form').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var btn = f.querySelector('button[type="submit"]');
      var msg = f.querySelector('.ds-form-msg');
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = btn.dataset.sending || label; }
      fetch(f.action, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(f) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.success) throw new Error('fail');
          msg.classList.remove('ds-err'); msg.textContent = msg.dataset.ok; f.reset(); if (form) form.dispatchEvent(new Event('change'));
        })
        .catch(function () { msg.classList.add('ds-err'); msg.textContent = msg.dataset.err; })
        .then(function () { if (btn) { btn.disabled = false; btn.textContent = label; } });
    });
  });
})();
