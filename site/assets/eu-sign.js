// EU-miner agreement form. CSP allows only self-hosted scripts: no inline code, no eval, no innerHTML with data.
(function () {
  'use strict';
  var root = document.getElementById('eu-sign');
  if (!root) return;
  var API = '/api/eu/';
  var form = document.getElementById('eu-agreement-form');
  var errBox = document.getElementById('eu-errors');
  var panel = document.getElementById('eu-review-panel');
  var done = document.getElementById('eu-done');
  var acceptBtn = document.getElementById('eu-accept');
  var chkAuthority = document.getElementById('eu-authority');
  var chkRead = document.getElementById('eu-read');
  var reviewedHash = '';
  var busy = false;

  var ROWS = {
    dc_locations: { cols: [['provider', 'Provider', 200], ['city', 'City', 200], ['country', 'Country', 0]], keep: 1 },
    hotkeys: { cols: [['value', 'SS58 hotkey address', 60]], scalar: true, keep: 0 },
    endpoints: { cols: [['value', 'host:port', 260]], scalar: true, keep: 0 },
    own_subprocessors: { cols: [['name', 'Name', 200], ['service', 'Service', 300], ['location', 'Location', 200]], keep: 0 }
  };
  var LABELS = {
    miner_company: 'Company name', miner_legal_form: 'Legal form', miner_address: 'Registered address',
    miner_country: 'Country', miner_register: 'Commercial register', miner_vat_id: 'VAT ID',
    signatory_name: 'Signatory name', signatory_role: 'Role', signatory_email: 'Email',
    privacy_contact: 'Privacy contact', dc_locations: 'Data-centre locations', hotkeys: 'Hotkeys',
    endpoints: 'Endpoints', own_subprocessors: 'Sub-processors', tom_statement: 'Measures',
    authority_confirmed: 'Authority', terms_read: 'Confirmation', text_sha256: 'Review'
  };

  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text) n.textContent = text;
    return n;
  }

  function addRow(key, values) {
    var spec = ROWS[key];
    var holder = root.querySelector('[data-rows="' + key + '"]');
    var row = el('div', { 'class': 'eu-row' });
    spec.cols.forEach(function (col) {
      var input;
      if (col[0] === 'country') {
        input = el('select', { 'aria-label': col[1] });
        Array.prototype.forEach.call(document.getElementById('miner_country').options, function (o) {
          input.appendChild(el('option', { value: o.value }, o.text));
        });
      } else {
        input = el('input', { type: 'text', 'aria-label': col[1], placeholder: col[1], maxlength: String(col[2]) });
      }
      input.setAttribute('data-col', col[0]);
      if (values && values[col[0]]) input.value = values[col[0]];
      row.appendChild(input);
    });
    var rm = el('button', { type: 'button', 'class': 'eu-remove', 'aria-label': 'Remove row' }, 'Remove');
    rm.addEventListener('click', function () { row.remove(); invalidate(); });
    row.appendChild(rm);
    holder.appendChild(row);
    return row;
  }

  function readRows(key) {
    var spec = ROWS[key];
    var out = [];
    root.querySelectorAll('[data-rows="' + key + '"] .eu-row').forEach(function (row) {
      var item = {};
      var any = false;
      row.querySelectorAll('[data-col]').forEach(function (input) {
        var v = input.value.trim();
        item[input.getAttribute('data-col')] = v;
        if (v) any = true;
      });
      if (!any) return;
      out.push(spec.scalar ? item.value : item);
    });
    return out;
  }

  function val(id) { return document.getElementById(id).value.trim(); }

  function collect() {
    var lang = form.querySelector('input[name="lang"]:checked').value;
    var data = { lang: lang, website: val('website') };
    ['miner_company', 'miner_legal_form', 'miner_address', 'miner_country', 'miner_register', 'miner_vat_id',
      'signatory_name', 'signatory_role', 'signatory_email', 'privacy_contact', 'tom_statement'].forEach(function (id) {
      data[id] = val(id);
    });
    Object.keys(ROWS).forEach(function (key) { data[key] = readRows(key); });
    return data;
  }

  function showErrors(title, fields) {
    errBox.textContent = '';
    errBox.appendChild(el('strong', {}, title));
    var keys = Object.keys(fields || {});
    if (keys.length) {
      var ul = el('ul');
      keys.forEach(function (k) {
        var base = k.split('[')[0].split('.')[0];
        ul.appendChild(el('li', {}, (LABELS[base] || k) + ': ' + fields[k]));
        var field = document.getElementById(base);
        if (field) field.setAttribute('aria-invalid', 'true');
      });
      errBox.appendChild(ul);
    }
    errBox.hidden = false;
    errBox.focus();
  }

  function clearErrors() {
    errBox.hidden = true;
    errBox.textContent = '';
    form.querySelectorAll('[aria-invalid]').forEach(function (n) { n.removeAttribute('aria-invalid'); });
  }

  function post(path, body) {
    return fetch(API + path, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), credentials: 'omit'
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; });
    });
  }

  function failure(res) {
    var b = res.body || {};
    if (res.status === 422) return showErrors(b.message || 'Please correct the highlighted fields.', b.fields);
    if (res.status === 429) return showErrors('Too many submissions from your network. Please try again later.');
    if (res.status === 409) { invalidate(); return showErrors(b.message || 'The agreement text changed; please review again.'); }
    if (res.status === 503) return showErrors('The signing service is temporarily unavailable. Please try again later.');
    showErrors('Something went wrong (' + res.status + '). Please try again.');
  }

  function invalidate() {
    reviewedHash = '';
    panel.hidden = true;
    chkAuthority.checked = false;
    chkRead.checked = false;
    acceptBtn.disabled = true;
  }

  function syncAccept() { acceptBtn.disabled = busy || !(reviewedHash && chkAuthority.checked && chkRead.checked); }

  Object.keys(ROWS).forEach(function (key) {
    root.querySelector('[data-add="' + key + '"]').addEventListener('click', function () {
      addRow(key).querySelector('input,select').focus();
      invalidate();
    });
    for (var i = 0; i < Math.max(ROWS[key].keep, 0); i++) addRow(key);
  });
  form.addEventListener('input', invalidate);
  form.addEventListener('change', invalidate);
  form.addEventListener('submit', function (e) { e.preventDefault(); });
  chkAuthority.addEventListener('change', syncAccept);
  chkRead.addEventListener('change', syncAccept);

  document.getElementById('eu-review').addEventListener('click', function () {
    if (busy) return;
    clearErrors();
    busy = true;
    post('preview', collect()).then(function (res) {
      busy = false;
      if (res.status !== 200) return failure(res);
      reviewedHash = res.body.text_sha256;
      document.getElementById('eu-text').textContent = res.body.text;
      document.getElementById('eu-sha').textContent = res.body.text_sha256;
      chkAuthority.checked = false;
      chkRead.checked = false;
      panel.hidden = false;
      syncAccept();
      document.getElementById('eu-review-title').focus();
    }).catch(function () { busy = false; showErrors('Network error. Please try again.'); });
  });

  acceptBtn.addEventListener('click', function () {
    if (busy || !reviewedHash) return;
    clearErrors();
    busy = true;
    syncAccept();
    var body = collect();
    body.text_sha256 = reviewedHash;
    body.authority_confirmed = chkAuthority.checked;
    body.terms_read = chkRead.checked;
    post('accept', body).then(function (res) {
      busy = false;
      if (res.status !== 201) { syncAccept(); return failure(res); }
      form.hidden = true;
      panel.hidden = true;
      document.getElementById('eu-done-id').textContent = res.body.agreement_id;
      var link = document.getElementById('eu-done-pdf');
      link.setAttribute('href', res.body.pdf_url);
      done.hidden = false;
      document.getElementById('eu-done-title').focus();
    }).catch(function () { busy = false; syncAccept(); showErrors('Network error. Please try again.'); });
  });

  // Inquiry form
  var cStatus = document.getElementById('eu-contact-status');
  document.getElementById('eu-contact-form').addEventListener('submit', function (e) { e.preventDefault(); });
  document.getElementById('eu-contact-send').addEventListener('click', function () {
    var btn = this;
    btn.disabled = true;
    var body = {
      company: val('c_company'), name: val('c_name'), email: val('c_email'), country: val('c_country'),
      gpus: val('c_gpus'), message: val('c_message'), website: val('c_website')
    };
    post('contact', body).then(function (res) {
      btn.disabled = false;
      cStatus.hidden = false;
      if (res.status === 201) { cStatus.textContent = 'Thank you. We will get back to you by email.'; return; }
      var f = (res.body && res.body.fields) || {};
      var msgs = Object.keys(f).map(function (k) { return k + ': ' + f[k]; });
      cStatus.textContent = res.status === 429 ? 'Too many submissions. Please try again later.'
        : msgs.length ? msgs.join(' · ') : 'Could not send (' + res.status + ').';
    }).catch(function () { btn.disabled = false; cStatus.hidden = false; cStatus.textContent = 'Network error. Please try again.'; });
  });
})();
