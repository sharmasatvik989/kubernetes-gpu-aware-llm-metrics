const $ = selector => document.querySelector(selector);
const useCase = $('#use-case');
const model = $('#model');
const tokens = $('#tokens');
const rps = $('#rps');
const slo = $('#slo');
const mode = $('#mode');
const cache = $('#cache');
const batch = $('#batch');
const maxPods = $('#max-pods');
const threads = $('#threads');
const podTemplate = $('#pod-template');
let catalog = { use_cases: [], models: [] };
let updateTimer;

const number = value => new Intl.NumberFormat('en-US').format(value);

function populateModels() {
  const matches = catalog.models.filter(item => item.use_case === useCase.value);
  model.innerHTML = matches.map(item => `<option value="${item.id}">${item.name}</option>`).join('');
  renderModelProfile();
  schedulePlan(0);
}

function renderModelProfile() {
  const selected = catalog.models.find(item => item.id === model.value);
  if (!selected) return;
  $('#model-profile').innerHTML = `<span>${selected.gpu}</span><span>${selected.weight_memory_gb} GB weights</span><span>${number(selected.tokens_per_second)} tok/s</span>`;
}

function syncOutputs() {
  $('#tokens-output').textContent = number(tokens.value);
  $('#cache-output').textContent = `${cache.value}%`;
  $('#max-pods-output').textContent = maxPods.value;
  $('#threads-output').textContent = threads.value;
  $('#slo-output').textContent = `${slo.value} ms`;
}

function renderMetrics(plan) {
  const items = [
    ['GPU pods', plan.replicas, `${number(plan.required_pods)} required`],
    ['Capacity gap', `${plan.capacity_deficit_percent}%`, `${number(plan.capacity_rps)} sustainable RPS`],
    ['Memory', `${plan.total_memory_gb} GB`, `${plan.memory_per_pod_gb} GB per pod`],
    ['Projected p95', `${plan.projected_latency_ms} ms`, `${plan.network_latency_ms} ms network`],
    ['Gateways', plan.gateway_instances, `${plan.gateway_threads} threads each`],
  ];
  $('#metrics').innerHTML = items.map(([label, value, detail]) => `<article class="plan-metric"><span>${label}</span><strong>${value}</strong><small>${detail}</small></article>`).join('');
}

function renderTraffic(traffic) {
  const nodes = [
    ['Ingress', traffic.incoming_rps, 'incoming'],
    ['Cache', traffic.cache_rps, 'served'],
    ['GPU admitted', traffic.admitted_rps, 'admitted'],
    ['Queued', traffic.queued_rps, 'queued'],
    ['Rejected', traffic.rejected_rps, 'rejected'],
  ];
  $('#traffic-flow').innerHTML = nodes.map(([label, value, type], index) => `${index ? '<i>→</i>' : ''}<div class="flow-node ${type}"><span>${label}</span><strong>${number(value)}</strong><small>requests/sec</small></div>`).join('');
}

function renderPods(data) {
  const canvas = $('#pods');
  canvas.innerHTML = '';
  data.pods.slice(0, 18).forEach((pod, index) => {
    const node = podTemplate.content.cloneNode(true);
    node.querySelector('.pod').style.setProperty('--delay', `${index * 35}ms`);
    node.querySelector('.pod-head strong').textContent = pod.name;
    node.querySelector('.zone').textContent = pod.zone;
    node.querySelector('.gpu-chip').textContent = `${data.plan.gpu} · ${pod.gpu_allocation} GPU`;
    node.querySelector('.util').textContent = `${pod.utilization}%`;
    node.querySelector('.bar i').style.width = `${pod.utilization}%`;
    node.querySelector('.memory').textContent = `${pod.memory_gb} GB`;
    canvas.append(node);
  });
  if (data.pods.length > 18) {
    canvas.insertAdjacentHTML('beforeend', `<div class="pod pod-overflow"><strong>+${data.pods.length - 18} pods</strong><span>Additional replicas managed by the autoscaler</span></div>`);
  }
  $('#pod-count').textContent = `${data.pods.length} running pods across ${Math.min(3, data.pods.length)} zones`;
}

function renderResources(plan) {
  const resources = [
    ['GPU type', plan.gpu],
    ['GPU per pod', plan.gpu_fraction_per_pod],
    ['Batch size', plan.batch_size],
    ['Batch efficiency', `${plan.batch_efficiency}×`],
    ['Network load', `${plan.network_mbps} Mbps`],
    ['Queue delay', `${plan.queue_delay_ms} ms`],
    ['GPU utilization', `${plan.gpu_utilization}%`],
  ];
  $('#resources').innerHTML = resources.map(([key, value]) => `<div><span>${key}</span><strong>${value}</strong></div>`).join('');
}

function renderPlan(data) {
  $('#plan-title').textContent = `${data.model.task} · ${data.model.name}`;
  const badge = $('#slo-badge');
  badge.textContent = data.plan.slo_status === 'within-slo' ? 'Within latency SLO' : 'Latency SLO at risk';
  badge.className = `slo-badge ${data.plan.slo_status}`;
  renderMetrics(data.plan);
  renderTraffic(data.traffic);
  renderPods(data);
  renderResources(data.plan);
  $('#why').innerHTML = data.why.map(item => `<li>${item}</li>`).join('');
}

async function updatePlan() {
  syncOutputs();
  const response = await fetch('/api/plan', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      model: model.value,
      tokens: Number(tokens.value),
      incoming_rps: Number(rps.value),
      latency_slo_ms: Number(slo.value),
      processing_mode: mode.value,
      gateway_threads: Number(threads.value),
      cache_hit_percent: Number(cache.value),
      batch_size: Number(batch.value),
      max_gpu_pods: Number(maxPods.value),
      queue_capacity: 100000,
    }),
  });
  if (!response.ok) throw new Error('Planner unavailable');
  renderPlan(await response.json());
}

function schedulePlan(delay = 120) {
  clearTimeout(updateTimer);
  updateTimer = setTimeout(() => updatePlan().catch(() => {
    $('#plan-title').textContent = 'Capacity planner unavailable';
  }), delay);
}

async function initialize() {
  const response = await fetch('/api/catalog');
  if (!response.ok) throw new Error('Catalog unavailable');
  catalog = await response.json();
  useCase.innerHTML = catalog.use_cases.map(item => `<option value="${item.id}">${item.name}</option>`).join('');
  populateModels();
}

useCase.addEventListener('change', populateModels);
model.addEventListener('change', () => { renderModelProfile(); schedulePlan(0); });
[tokens, rps, slo, cache, maxPods, threads].forEach(input => input.addEventListener('input', () => {
  syncOutputs();
  schedulePlan();
}));
[mode, batch].forEach(input => input.addEventListener('change', () => schedulePlan(0)));
document.querySelectorAll('[data-rps]').forEach(button => button.addEventListener('click', () => {
  rps.value = button.dataset.rps;
  schedulePlan(0);
}));

initialize().catch(() => {
  $('#plan-title').textContent = 'Capacity planner unavailable';
});
