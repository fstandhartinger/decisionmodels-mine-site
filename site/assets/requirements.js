// Shared, read-only verdict logic for the widget and WebMCP. Thresholds come from mine.json.
(() => {
  const osValues = ['linux', 'windows', 'macos'];
  window.MiningRequirements = {
    check(data, os, gpuVramGb, vendor = 'NVIDIA') {
      if (!osValues.includes(os)) throw new Error('Unsupported OS');
      if (typeof gpuVramGb !== 'number' || !Number.isFinite(gpuVramGb) || gpuVramGb < 0 || gpuVramGb > 1024) throw new Error('Invalid GPU VRAM');
      const pool = data.pools.find(p => p.id === 's1-fast');
      const gpuPools = data.pools.filter(p => p.enabled_at_launch && p.gpu.count > 0 && vendor === p.gpu.vendor && gpuVramGb >= p.gpu.min_vram_gb);
      const eligiblePools = [...gpuPools, ...data.pools.filter(p => p.enabled_at_launch && p.gpu.count === 0)].map(p => p.id);
      const smallest = data.pools.filter(p => p.enabled_at_launch && p.gpu.count > 0).reduce((a, p) => Math.min(a, p.gpu.min_vram_gb), Infinity);
      const reasons = [];
      const support = data.os_support[os];
      if (support.mining === 'remote_only') reasons.push('This Mac can check readiness or control an authorized NVIDIA Linux host; it cannot mine this release locally.');
      if (!gpuPools.length) reasons.push(`A GPU pool needs a compatible ${pool.gpu.vendor} GPU with at least ${smallest} GB VRAM (s1-fast ${pool.gpu.min_vram_gb} GB). Without one, only the CPU pool (s1-cpu) fits. ${data.copy.GPU_NOTE}`);
      if (support.mining === 'conditional') reasons.push(support.caveat);
      const hardwareCandidate = support.mining !== 'remote_only' && gpuPools.length > 0;
      if (hardwareCandidate) reasons.push(`Your GPU capacity is a candidate for ${gpuPools.map(p => p.id).join(', ')}. The agent must still verify ${data.requirements.driver_min}, CPU/RAM/disk, container and model health, clock and public TCP ingress.`);
      reasons.push(data.copy.CHECKER_BODY);
      return { verdict: hardwareCandidate ? (support.mining === 'conditional' ? 'Conditional WSL2 candidate' : (data.status.live ? 'Hardware candidate; verify runtime' : 'Hardware candidate for launch')) : data.copy.OTHER_HOST, reasons, hardware_candidate: hardwareCandidate, eligible_pools: support.mining === 'remote_only' ? [] : eligiblePools, live: data.status.live, guide: support.guide };
    }
  };
})();
