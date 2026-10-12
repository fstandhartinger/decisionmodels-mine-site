# Accept the EU-miner agreement

If your company is established in the EU or EEA and operates REAX miners, you can accept our standing offer of a sub-processing agreement under Art. 28(4) GDPR electronically. This page is the signing form; the requirements and the process are explained on the [EU miner page](/eu). Accepting the agreement does not mean that EU-tier traffic will be routed to you; EU routing is switched off until the first verified EU miner.

<!--eu-form:start-->
<div id="eu-sign" class="eu-sign">
<noscript><p class="eu-alert">This form needs JavaScript. Without it, use the HTTP API described below.</p></noscript>
<p class="eu-callout"><strong>An AI agent may help fill this in, but an authorised person must review and click Accept.</strong> Accepting concludes a legally binding agreement on behalf of your company.</p>
<form id="eu-agreement-form" novalidate autocomplete="on">
<fieldset class="eu-set"><legend>Agreement language</legend>
<label class="eu-inline"><input type="radio" name="lang" value="en" checked> English</label>
<label class="eu-inline"><input type="radio" name="lang" value="de"> Deutsch</label>
<p class="eu-hint">The selected language version is the binding text you accept.</p></fieldset>
<fieldset class="eu-set"><legend>Your company</legend>
<div class="eu-field"><label for="miner_company">Company name</label><input id="miner_company" name="miner_company" type="text" required autocomplete="organization" maxlength="200"></div>
<div class="eu-field"><label for="miner_legal_form">Legal form</label><span class="eu-hint" id="miner_legal_form-hint">e.g. GmbH, SARL, B.V.</span><input id="miner_legal_form" name="miner_legal_form" type="text" required aria-describedby="miner_legal_form-hint" maxlength="100"></div>
<div class="eu-field"><label for="miner_address">Registered address</label><textarea id="miner_address" name="miner_address" rows="4" required autocomplete="street-address" maxlength="500"></textarea></div>
<div class="eu-field"><label for="miner_country">Country of establishment</label><span class="eu-hint" id="miner_country-hint">EU/EEA only.</span><select id="miner_country" name="miner_country" required aria-describedby="miner_country-hint"><option value="">Select…</option><option value="AT">Austria (AT)</option><option value="BE">Belgium (BE)</option><option value="BG">Bulgaria (BG)</option><option value="HR">Croatia (HR)</option><option value="CY">Cyprus (CY)</option><option value="CZ">Czechia (CZ)</option><option value="DK">Denmark (DK)</option><option value="EE">Estonia (EE)</option><option value="FI">Suomi (FI)</option><option value="FR">France (FR)</option><option value="DE">Germany (DE)</option><option value="GR">Greece (GR)</option><option value="HU">Hungary (HU)</option><option value="IS">Iceland (IS)</option><option value="IE">Ireland (IE)</option><option value="IT">Italy (IT)</option><option value="LV">Latvia (LV)</option><option value="LI">Liechtenstein (LI)</option><option value="LT">Lithuania (LT)</option><option value="LU">Luxembourg (LU)</option><option value="MT">Malta (MT)</option><option value="NL">Netherlands (NL)</option><option value="NO">Norway (NO)</option><option value="PL">Poland (PL)</option><option value="PT">Portugal (PT)</option><option value="RO">Romania (RO)</option><option value="SK">Slovakia (SK)</option><option value="SI">Slovenia (SI)</option><option value="ES">Spain (ES)</option><option value="SE">Sweden (SE)</option></select></div>
<div class="eu-field"><label for="miner_register">Commercial register and number</label><span class="eu-hint" id="miner_register-hint">e.g. HRB 123456, Amtsgericht München</span><input id="miner_register" name="miner_register" type="text" required aria-describedby="miner_register-hint" maxlength="200"></div>
<div class="eu-field"><label for="miner_vat_id">VAT ID (optional)</label><input id="miner_vat_id" name="miner_vat_id" type="text" maxlength="50"></div>
</fieldset>
<fieldset class="eu-set"><legend>Authorised signatory</legend>
<div class="eu-field"><label for="signatory_name">Full name</label><input id="signatory_name" name="signatory_name" type="text" required autocomplete="name" maxlength="200"></div>
<div class="eu-field"><label for="signatory_role">Role / title</label><span class="eu-hint" id="signatory_role-hint">e.g. Managing Director</span><input id="signatory_role" name="signatory_role" type="text" required aria-describedby="signatory_role-hint" autocomplete="organization-title" maxlength="200"></div>
<div class="eu-field"><label for="signatory_email">Email</label><input id="signatory_email" name="signatory_email" type="email" required autocomplete="email" maxlength="254"></div>
<div class="eu-field"><label for="privacy_contact">Privacy contact (email or name)</label><span class="eu-hint" id="privacy_contact-hint">Who answers data-protection questions.</span><input id="privacy_contact" name="privacy_contact" type="text" required aria-describedby="privacy_contact-hint" maxlength="254"></div>
</fieldset>
<fieldset class="eu-set"><legend>Data-centre locations</legend><p class="eu-hint">Where inference runs (EU/EEA only). At least one.</p><div class="eu-rows" data-rows="dc_locations"></div><button type="button" class="eu-add" data-add="dc_locations">Add location</button></fieldset>
<fieldset class="eu-set"><legend>Hotkeys (SS58)</legend><p class="eu-hint">Operational hotkey addresses of your miners; they are linked to this agreement. Never enter seeds or coldkeys.</p><div class="eu-rows" data-rows="hotkeys"></div><button type="button" class="eu-add" data-add="hotkeys">Add hotkey</button></fieldset>
<fieldset class="eu-set"><legend>Public endpoints</legend><p class="eu-hint">host:port of your miner endpoints (optional).</p><div class="eu-rows" data-rows="endpoints"></div><button type="button" class="eu-add" data-add="endpoints">Add endpoint</button></fieldset>
<fieldset class="eu-set"><legend>Your own sub-processors</legend><p class="eu-hint">Hosting or other providers you use for this processing (optional).</p><div class="eu-rows" data-rows="own_subprocessors"></div><button type="button" class="eu-add" data-add="own_subprocessors">Add sub-processor</button></fieldset>
<fieldset class="eu-set"><legend>Technical and organisational measures</legend>
<div class="eu-field"><label for="tom_statement">Describe your measures</label><span class="eu-hint" id="tom_statement-hint">Encryption, access control, logging, physical security, incident handling. Max. 4000 characters.</span><textarea id="tom_statement" name="tom_statement" rows="8" required aria-describedby="tom_statement-hint" maxlength="4000"></textarea></div>
</fieldset>
<div class="eu-hp" aria-hidden="true"><label for="website">Leave this field empty</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<div id="eu-errors" class="eu-alert" role="alert" tabindex="-1" hidden></div>
<p><button type="button" id="eu-review" class="eu-primary">Review agreement</button></p>
</form>
<section id="eu-review-panel" class="eu-panel" aria-labelledby="eu-review-title" hidden>
<h2 id="eu-review-title" tabindex="-1">Review the agreement</h2>
<p>This is the exact text you accept. Scroll through it before continuing.</p>
<pre id="eu-text" class="eu-text" tabindex="0" aria-label="Agreement text"></pre>
<p class="eu-hint">SHA-256 of this text: <code id="eu-sha"></code></p>
<label class="eu-check"><input type="checkbox" id="eu-authority"> I am authorised to bind the company named above to this agreement.</label>
<label class="eu-check"><input type="checkbox" id="eu-read"> I have read the agreement text above and accept it.</label>
<p><button type="button" id="eu-accept" class="eu-primary" disabled>Accept agreement</button></p>
</section>
<section id="eu-done" class="eu-panel eu-ok" aria-labelledby="eu-done-title" hidden>
<h2 id="eu-done-title" tabindex="-1">Agreement accepted</h2>
<p>Agreement ID: <code id="eu-done-id"></code></p>
<p><a id="eu-done-pdf" class="eu-primary" href="#" download>Download your PDF copy</a></p>
<p><strong>Save this PDF; it is your copy.</strong> The link is private to you and is not shown again. We verify the company, the data-centre locations and your hotkeys before any EU-tier traffic could be routed to you (routing is switched off until the first verified EU miner and is not promised), and contact you at the signatory e-mail address.</p>
</section>
<section class="eu-panel" aria-labelledby="eu-contact-title">
<h2 id="eu-contact-title">Not ready to sign? Talk to us</h2>
<form id="eu-contact-form" novalidate>
<div class="eu-field"><label for="c_company">Company</label><input id="c_company" name="c_company" type="text" required maxlength="200"></div>
<div class="eu-field"><label for="c_name">Your name</label><input id="c_name" name="c_name" type="text" required maxlength="200"></div>
<div class="eu-field"><label for="c_email">Email</label><input id="c_email" name="c_email" type="email" required maxlength="254"></div>
<div class="eu-field"><label for="c_country">Country (optional)</label><input id="c_country" name="c_country" type="text" maxlength="100"></div>
<div class="eu-field"><label for="c_gpus">GPUs / capacity (optional)</label><input id="c_gpus" name="c_gpus" type="text" maxlength="300"></div>
<div class="eu-field"><label for="c_message">Message (optional)</label><textarea id="c_message" name="c_message" rows="4" maxlength="4000"></textarea></div>
<div class="eu-hp" aria-hidden="true"><label for="c_website">Leave this field empty</label><input id="c_website" type="text" tabindex="-1" autocomplete="off"></div>
<div id="eu-contact-status" class="eu-alert" role="status" hidden></div>
<p><button type="button" id="eu-contact-send">Send inquiry</button></p>
</form>
</section>
</div>
<script src="/assets/eu-sign.js" defer></script>
<!--eu-form:end-->

## For agents: the HTTP API

An agent may prepare the data, but a person with signing authority must read the text and accept. The same flow is available as JSON over HTTPS:

1. `GET /api/eu/agreement?lang=en|de` returns the template with its version and SHA-256.
2. `POST /api/eu/preview` with the fields below returns the exact rendered `text` and its `text_sha256`.
3. After the authorised person has reviewed that text, `POST /api/eu/accept` with the same fields plus `text_sha256`, `authority_confirmed: true`, `terms_read: true` and an empty `website` stores the agreement and returns `agreement_id` and a private `pdf_url`.

Fields: `lang`, `miner_company`, `miner_legal_form`, `miner_address`, `miner_country` (EU/EEA ISO code), `miner_register`, `miner_vat_id` (optional), `signatory_name`, `signatory_role`, `signatory_email`, `privacy_contact`, `dc_locations` (list of `provider`, `city`, `country`), `hotkeys` (SS58 list), `endpoints` (`host:port` list, optional), `own_subprocessors` (list of `name`, `service`, `location`, optional), `tom_statement` (max. 4000 characters). Unknown fields are rejected. Submissions are limited to 5 per IP per hour.
