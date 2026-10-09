// Shared, read-only verdict logic for the widget and WebMCP. Thresholds come from mine.json.
(() => {
  const osValues = ['linux', 'windows', 'macos'];
  window.MiningRequirements = {
    check(data, os, gpuVramGb, vendor = 'NVIDIA') {
      if (!osValues.includes(os)) throw new Error('Unsupported OS');
      if (typeof gpuVramGb !== 'number' || !Number.isFinite(gpuVramGb) || gpuVramGb < 0 || gpuVramGb > 1024) throw new Error('Invalid GPU VRAM');
      const pool = data.pools.find(p => p.id === 's1-fast');
      const reasons = [];
      const support = data.os_support[os];
      if (support.mining === 'remote_only') reasons.push('This Mac can check readiness or control an authorized NVIDIA Linux host; it cannot mine this release locally.');
      if (vendor !== pool.gpu.vendor || gpuVramGb < pool.gpu.min_vram_gb) reasons.push(`This release needs a compatible ${pool.gpu.vendor} GPU with at least ${pool.gpu.min_vram_gb} GB VRAM. ${data.copy.GPU_NOTE}`);
      if (support.mining === 'conditional') reasons.push(support.caveat);
      const hardwareCandidate = support.mining !== 'remote_only' && vendor === pool.gpu.vendor && gpuVramGb >= pool.gpu.min_vram_gb;
      if (hardwareCandidate) reasons.push(`Your GPU capacity is a candidate for s1-fast. The agent must still verify ${data.requirements.driver_min}, CPU/RAM/disk, container and model health, clock and public TCP ingress.`);
      reasons.push(data.copy.CHECKER_BODY);
      return { verdict: hardwareCandidate ? (support.mining === 'conditional' ? 'Conditional WSL2 candidate' : (data.status.live ? 'Hardware candidate; verify runtime' : 'Hardware candidate for launch')) : data.copy.OTHER_HOST, reasons, hardware_candidate: hardwareCandidate, live: data.status.live, guide: support.guide };
    }
  };
})();
