// Optional read-only WebMCP. No actions, wallet access, supplied URLs or command inputs.
(() => {
  const context = document.modelContext || navigator.modelContext;
  if (!context || typeof context.registerTool !== 'function') return;
  let cache;
  const data = () => {
    if (!cache) cache = fetch('/mine.json', { credentials: 'omit' }).then(r => { if (!r.ok) throw new Error('mine.json unavailable'); return r.json(); }).catch(e => { cache = null; throw e; });
    return cache;
  };
  const empty = { type: 'object', properties: {}, additionalProperties: false };
  const enums = (name, values) => ({ type: 'object', properties: { [name]: { type: 'string', enum: values } }, required: [name], additionalProperties: false });
  const validate = (value, allowed) => { if (!allowed.includes(value)) throw new Error('Invalid enum input'); return value; };
  const osEnum = ['linux', 'windows', 'macos'];
  const tools = [
    { name: 'get_mining_status', description: 'Read the REAX launch status and pinned kit integrity.', inputSchema: empty, execute: async () => { const d = await data(); return { state: d.state, source: d.source, status: d.status, integrity: d.integrity }; } },
    { name: 'get_agent_prompt', description: 'Get a setup prompt for a local coding agent, with human permissions preserved.', inputSchema: enums('variant', ['short', 'safe', 'guided']), execute: async ({ variant }) => { validate(variant, ['short','safe','guided']); const d = await data(); return { prompt: d.prompts[variant], guide: d.links.agent }; } },
    { name: 'check_requirements', description: 'Check OS and NVIDIA VRAM capacity against the pinned release; all other hardware and network checks remain required.', inputSchema: { type: 'object', properties: { os: { type: 'string', enum: osEnum }, gpu_vram_gb: { type: 'number', minimum: 0, maximum: 1024 } }, required: ['os', 'gpu_vram_gb'], additionalProperties: false }, execute: async ({ os, gpu_vram_gb }) => window.MiningRequirements.check(await data(), os, gpu_vram_gb) },
    { name: 'get_setup_steps', description: 'Read preparation steps before launch or practice and real-network steps once available. Before launch stop after doctor and plan; runtime commands are unavailable. Real registration requires human approval.', inputSchema: enums('mode', ['localnet','testnet','mainnet']), execute: async ({ mode }) => { validate(mode,['localnet','testnet','mainnet']); const d = await data(); return { mode, state: d.state, source: d.source, status: d.status, steps: mode === 'localnet' ? d.steps : d.mainnet_steps.map(s => ({ ...s, command: s.command && (mode === 'testnet' ? s.command.replace(' --confirm-mainnet', '') : s.command).replaceAll('mainnet', mode) })), rules: d.rules }; } },
    { name: 'get_wallet_guidance', description: 'Read OS-specific separate-device custody guidance; no wallet access or signing.', inputSchema: enums('os', osEnum), execute: async ({ os }) => { validate(os,osEnum); const d = await data(); return { guidance: d.os_support[os].wallet, guide: d.links.wallets, rules: d.rules }; } },
    { name: 'get_agent_rules', description: 'Read rules for custody, human payment approvals, launch holds and host identity.', inputSchema: empty, execute: async () => ({ rules: (await data()).rules }) }
  ];
  tools.forEach(tool => { try { context.registerTool({ ...tool, annotations: { readOnlyHint: true, consequentialHint: false } }); } catch (_) { /* One unsupported registration must not disable other tools. */ } });
})();
