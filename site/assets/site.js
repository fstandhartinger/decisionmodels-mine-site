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
      const tabs = [...document.querySelectorAll('.prompt-tab')];
      const choose = tab => {
        prompt.textContent = data.prompts[tab.dataset.variant];
        prompt.setAttribute('aria-labelledby', tab.id);
        tabs.forEach(other => {
          const selected = other === tab;
          other.setAttribute('aria-selected', String(selected));
          other.tabIndex = selected ? 0 : -1;
        });
        document.querySelector('.copy-status').textContent = '';
      };
      tabs.forEach(tab => {
        tab.hidden = false;
        tab.addEventListener('click', () => choose(tab));
        tab.addEventListener('keydown', event => {
          if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
          event.preventDefault();
          const index = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 :
            (tabs.indexOf(tab) + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
          choose(tabs[index]); tabs[index].focus();
        });
      });
    }
    if (checker) {
      checker.hidden = false;
      const os = checker.querySelector('#os'), gpu = checker.querySelector('#gpu');
      const buttons = checker.querySelectorAll('.guide-actions button');
      buttons.forEach(button => { button.hidden = true; });
      const update = () => {
        const verdict = document.querySelector('#verdict');
        verdict.replaceChildren(); verdict.hidden = !os.value || !gpu.value;
        if (verdict.hidden) return;
        const value = gpu.value;
        const sizes = { none: 0, lt16: 8, '16': 16, '24': 24, '48': 48, amd: 0, apple: 0 };
        const vendor = value === 'amd' ? 'AMD' : value === 'apple' ? 'Apple' : 'NVIDIA';
        const result = window.MiningRequirements.check(data, os.value, sizes[value], vendor);
        const sentence = document.createElement('p');
        const status = data.status.live ? 'verify runtime before mining' : 'the network is not live yet';
        sentence.textContent = os.value === 'macos'
          ? `This Mac cannot mine locally; use an authorized NVIDIA Linux host (${status}).`
          : result.hardware_candidate
            ? (os.value === 'windows'
              ? `This GPU is a conditional WSL2 candidate, not yet tested by us end to end; ${status}.`
              : `This GPU meets the capacity requirement; ${status}.`)
            : `Mining needs another host with a compatible NVIDIA GPU of at least 24 GB; ${status}.`;
        verdict.append(sentence);
        const link = document.createElement('a'); link.id = 'os-guide'; link.href = result.guide; link.textContent = `Read the ${os.options[os.selectedIndex].text} guide →`; verdict.append(link);
        checker.action = result.guide;
      };
      checker.addEventListener('change', update);
      checker.addEventListener('submit', event => {
        event.preventDefault();
        // Declarative tool calls can read the verdict without navigating.
        update();
        if (event.agentInvoked && typeof event.respondWith === 'function') { event.preventDefault(); event.respondWith(Promise.resolve(document.querySelector('#verdict').textContent)); }
      });
      update();
    }
  }).catch(() => { const status = document.querySelector('.copy-status'); if (status) status.textContent = 'Live data unavailable. The prompt and OS guide links still work.'; });
})();
