(() => {
  const theme = document.querySelector('.theme-toggle');
  theme.hidden = false;
  const modes = ['auto', 'light', 'dark'];
  function currentMode() { return document.documentElement.dataset.theme || 'auto'; }
  function labelTheme() {
    const mode = currentMode();
    theme.textContent = mode[0].toUpperCase() + mode.slice(1);
    theme.setAttribute('aria-label', `Switch color theme (current: ${mode})`);
  }
  labelTheme();
  theme.addEventListener('click', () => {
    const next = modes[(modes.indexOf(currentMode()) + 1) % modes.length];
    if (next === 'auto') delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = next;
    try { localStorage.setItem('dm-theme', next); } catch (_) {}
    labelTheme();
  });
  const sampleButtons = [...document.querySelectorAll('[data-sample]')];
  if (sampleButtons.length) {
    const choose = button => {
      sampleButtons.forEach(other => {
        const selected = other === button;
        other.setAttribute('aria-selected', String(selected));
        other.tabIndex = selected ? 0 : -1;
        document.getElementById('doctor-' + other.dataset.sample).hidden = !selected;
      });
    };
    sampleButtons.forEach(button => {
      button.hidden = false;
      button.addEventListener('click', () => choose(button));
      button.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        const index = event.key === 'Home' ? 0 : event.key === 'End' ? sampleButtons.length - 1 :
          (sampleButtons.indexOf(button) + (event.key === 'ArrowRight' ? 1 : -1) + sampleButtons.length) % sampleButtons.length;
        choose(sampleButtons[index]); sampleButtons[index].focus();
      });
    });
    choose(sampleButtons[0]);
  }
  async function copy(text, button, status) {
    try { await navigator.clipboard.writeText(text); if (status) status.textContent = 'Copied. Paste into your local coding agent.'; else button.textContent = 'Copied'; }
    catch (_) { if (status) status.textContent = 'Select the prompt text and copy it manually.'; else button.textContent = 'Select code to copy'; }
  }
  document.querySelectorAll('pre').forEach(pre => {
    const code = pre.querySelector('code');
    if (!code) return;
    const button = document.createElement('button'); button.type = 'button'; button.className = 'code-copy'; button.textContent = 'Copy code';
    button.setAttribute('aria-label', 'Copy this code block');
    button.addEventListener('click', () => copy(code.textContent, button)); pre.prepend(button);
  });
  document.querySelectorAll('.docs h2, .docs h3').forEach(h => {
    const who = h.textContent.startsWith('Human step') ? 'YOU' : h.textContent.startsWith('Agent step') ? 'AGENT' : null;
    if (who) { const chip = document.createElement('span'); chip.className = 'step-chip'; chip.textContent = who; h.prepend(chip); }
  });
  const prompt = document.querySelector('#agent-prompt');
  const checker = document.querySelector('.checker');
  if (!prompt && !checker) return;
  fetch('/mine.json', { credentials: 'omit' }).then(r => { if (!r.ok) throw new Error('Manifest unavailable'); return r.json(); }).then(data => {
    if (prompt) {
      const copyButton = document.querySelector('#copy-prompt'); copyButton.hidden = false;
      copyButton.addEventListener('click', () => copy(prompt.textContent, copyButton, document.querySelector('.copy-status')));
      document.querySelectorAll('.prompt-tab').forEach(tab => {
        tab.hidden = false;
        tab.addEventListener('click', () => {
          prompt.textContent = data.prompts[tab.dataset.variant];
          document.querySelectorAll('.prompt-tab').forEach(other => other.setAttribute('aria-pressed', String(other === tab)));
          document.querySelector('.copy-status').textContent = '';
        });
      });
    }
    if (checker) {
      const os = checker.querySelector('#os'), gpu = checker.querySelector('#gpu');
      const buttons = checker.querySelectorAll('.guide-actions button');
      buttons.forEach((button, i) => { button.hidden = i !== 0; });
      const update = () => {
        const value = gpu.value;
        const sizes = { none: 0, lt16: 8, '16': 16, '24': 24, '48': 48, amd: 0, apple: 0 };
        const vendor = value === 'amd' ? 'AMD' : value === 'apple' ? 'Apple' : 'NVIDIA';
        const result = window.MiningRequirements.check(data, os.value, sizes[value], vendor);
        const verdict = document.querySelector('#verdict');
        verdict.replaceChildren();
        const strong = document.createElement('strong'); strong.textContent = result.verdict; verdict.append(strong);
        result.reasons.forEach(reason => { const p = document.createElement('p'); p.textContent = reason; verdict.append(p); });
        const link = document.createElement('a'); link.id = 'os-guide'; link.href = result.guide; link.textContent = `Read the ${os.options[os.selectedIndex].text} guide →`; verdict.append(link);
        checker.action = result.guide; buttons[0].setAttribute('formaction', result.guide); buttons[0].textContent = 'Open OS guide';
        checker.querySelector('.form-note').hidden = true;
      };
      checker.addEventListener('change', update);
      checker.addEventListener('submit', event => {
        // Human submit also navigates normally; declarative tool calls can read the result.
        update();
        if (event.agentInvoked && typeof event.respondWith === 'function') { event.preventDefault(); event.respondWith(Promise.resolve(document.querySelector('#verdict').textContent)); }
      });
      update();
    }
  }).catch(() => { const status = document.querySelector('.copy-status'); if (status) status.textContent = 'Live data unavailable. The prompt and OS guide links still work.'; });
})();
