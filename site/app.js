'use strict';
const report = JSON.parse(document.getElementById('case-data').textContent);
const queue = JSON.parse(document.getElementById('queue-data').textContent);
const knowledge = JSON.parse(document.getElementById('knowledge-data').textContent);
const byId = id => document.getElementById(id);
const put = (id, value) => { byId(id).textContent = value; };
const all = selector => [...document.querySelectorAll(selector)];
const selector = byId('case-select');
const caseButtons = all('[data-case]');
const phaseButtons = all('[data-phase]');
const oldVersion = report.metadata.old_version;
const currentVersion = report.metadata.current_version;
let selected = 'ENC-04';
let phase = 'before_review';
let activeControl = 'current_source';
let queueFilter = 'all';
const reasonLabels = { unsupported_claim: 'Unsupported claims', policy_changed: 'Changed policies', missing_citation: 'Missing citations', stale_provenance_only: 'Stale references' };
const explain = {
  policy_changed: 'The policy changed. Update the answer from the current source, then ask the owner to review it.',
  stale_provenance_only: 'The wording still matches. Confirm the current source and ask the owner to review the reference.',
  missing_citation: 'The claim matches, but the reference is missing. Add the evidence before owner review.',
  unsupported_claim: 'This source does not support the claim. Hold the answer and escalate for investigation.'
};
knowledge.policies.forEach(policy => {
  const option = document.createElement('option'); option.value = policy.id;
  option.textContent = `${policy.id} / ${policy.question}`; selector.append(option);
});
function context() {
  return {
    policy: knowledge.policies.find(item => item.id === selected),
    response: report.cases.find(item => item.policy_id === selected && item.phase === phase),
    task: queue.items.find(item => item.policy_id === selected)
  };
}
function renderControl() {
  const { policy, response } = context();
  const descriptions = {
    accurate: {
      title: 'Inside the claim check',
      explanation: 'The Python evaluator compares the example’s structured claim value with the current policy value. The sentences below show the context; the check does not interpret unrestricted prose.',
      leftLabel: 'ANSWER CLAIM', rightLabel: 'CURRENT POLICY', left: response.answer, right: policy.versions[currentVersion].answer
    },
    cited: {
      title: 'Inside the citation check',
      explanation: 'Does the example name the policy it is supposed to cite? This checks the policy ID. A matching ID alone does not prove that the document is authentic or the control exists.',
      leftLabel: 'CITED POLICY', rightLabel: 'EXPECTED POLICY', left: response.citation || 'No citation provided', right: policy.id
    },
    current_source: {
      title: 'Inside the version check',
      explanation: 'Does the answer refer to the current source snapshot? Even an unchanged policy needs a current reference. A current version does not replace owner approval.',
      leftLabel: 'ANSWER VERSION', rightLabel: 'CURRENT VERSION', left: response.source_version, right: currentVersion
    }
  };
  const info = descriptions[activeControl];
  put('control-title', info.title.toUpperCase()); put('control-explanation', info.explanation);
  put('control-left-label', info.leftLabel); put('control-right-label', info.rightLabel);
  put('control-left', info.left); put('control-right', info.right);
  all('[data-control]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.control === activeControl)));
  byId('control-inspector').dataset.outcome = response.evaluation[activeControl] ? 'pass' : 'review';
}
function render() {
  const { policy, response, task } = context();
  selector.value = selected;
  caseButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.case === selected)));
  phaseButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.phase === phase)));
  put('record-id', selected); put('question', policy.question);
  put('previous-source', policy.versions[oldVersion].answer); put('current-source', policy.versions[currentVersion].answer);
  put('source-context', task.source_changed ? 'The policy wording changed between these two snapshots.' : 'The policy wording is unchanged. The reference still belongs to a newer version.');
  document.querySelector('.source-diff').classList.toggle('is-unchanged', !task.source_changed);
  put('answer-label', phase === 'before_review' ? 'ORIGINAL ANSWER / SIMULATED EXAMPLE' : 'AFTER SOURCE REFRESH / SIMULATED EXAMPLE');
  put('answer', response.answer); put('citation', `Citation: ${response.citation || 'missing'} / Source version: ${response.source_version}`);
  const checks = byId('checks'); checks.replaceChildren();
  [['Claim matches current policy', 'accurate'], ['Citation names the correct policy', 'cited'], ['Source version is current', 'current_source']].forEach(([label, key]) => {
    const button = document.createElement('button'); button.type = 'button'; button.className = 'finding';
    button.dataset.control = key; button.setAttribute('aria-controls', 'control-inspector');
    const name = document.createElement('span'); name.textContent = label;
    const status = document.createElement('span'); const pass = response.evaluation[key];
    status.className = `status ${pass ? 'pass' : 'review'}`; status.textContent = pass ? 'MATCHES' : 'CHECK';
    const arrow = document.createElement('span'); arrow.className = 'finding-arrow'; arrow.textContent = '↗'; arrow.setAttribute('aria-hidden', 'true');
    button.append(name, status, arrow); button.addEventListener('click', () => { activeControl = key; renderControl(); }); checks.append(button);
  });
  put('review-action', phase === 'before_review' ? explain[task.reason] : 'These three checks now match the refreshed example. A security owner still needs to verify the evidence and approve any customer answer.');
  put('review-owner', `Proposed owner / ${task.owner}`);
  document.querySelector('.experiment').dataset.phase = phase;
  renderControl();
}
function chooseCase(id, scroll = false) {
  selected = id; phase = 'before_review';
  const task = queue.items.find(item => item.policy_id === selected);
  activeControl = task.reason === 'missing_citation' ? 'cited' : task.reason === 'stale_provenance_only' ? 'current_source' : 'accurate';
  render();
  if (scroll) byId('review').scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
}
caseButtons.forEach(button => button.addEventListener('click', () => chooseCase(button.dataset.case)));
phaseButtons.forEach(button => button.addEventListener('click', () => { phase = button.dataset.phase; render(); }));
selector.addEventListener('change', () => chooseCase(selector.value));
all('[data-count]').forEach(node => { node.textContent = queue.summary.by_reason[node.dataset.count] || 0; });
put('queue-total', `${queue.summary.blocked_pending_approval}/${queue.summary.total_answers_reviewed} original answers held.`);
function renderQueue() {
  const items = queueFilter === 'all' ? queue.items : queue.items.filter(item => item.reason === queueFilter);
  all('[data-queue-reason]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.queueReason === queueFilter)));
  put('preview-label', `${queueFilter === 'all' ? 'All review examples' : reasonLabels[queueFilter]} / showing ${Math.min(3, items.length)} of ${items.length}`);
  const list = byId('queue-preview-items'); list.replaceChildren();
  items.slice(0, 3).forEach(item => {
    const row = document.createElement('article'); row.className = 'preview-record';
    const identity = document.createElement('span'); identity.className = `preview-priority ${item.priority.toLowerCase()}`; identity.textContent = `${item.priority} / ${item.policy_id}`;
    const body = document.createElement('div'); const title = document.createElement('h3'); title.textContent = item.question;
    const owner = document.createElement('p'); owner.textContent = `Proposed owner: ${item.owner}`; body.append(title, owner);
    const button = document.createElement('button'); button.type = 'button'; button.textContent = 'Inspect example ↗';
    button.addEventListener('click', () => chooseCase(item.policy_id, true)); row.append(identity, body, button); list.append(row);
  });
  const link = byId('preview-full-link');
  link.href = queueFilter === 'all' ? 'review-queue.html' : `review-queue.html?reason=${encodeURIComponent(queueFilter)}`;
  link.textContent = queueFilter === 'all' ? `Open all ${queue.summary.total_answers_reviewed} review records ↗` : `Open the ${items.length} matching review record${items.length === 1 ? '' : 's'} ↗`;
}
all('[data-queue-reason]').forEach(button => button.addEventListener('click', () => { queueFilter = button.dataset.queueReason; renderQueue(); }));
renderQueue();

const table = document.createElement('table'); const caption = document.createElement('caption');
caption.textContent = 'Constructed examples / not a live AI benchmark'; table.append(caption);
const head = document.createElement('thead'); const headrow = document.createElement('tr');
['Defined check', 'Original examples', 'Refreshed examples'].forEach(label => { const cell = document.createElement('th'); cell.scope = 'col'; cell.textContent = label; headrow.append(cell); });
head.append(headrow); table.append(head);
const tbody = document.createElement('tbody');
[['Claim matches', 'accurate'], ['Correct citation', 'cited'], ['Current version', 'current_source'], ['All three checks match', 'publishable']].forEach(([label, key]) => {
  const row = document.createElement('tr'); const heading = document.createElement('th'); heading.scope = 'row'; heading.textContent = label; row.append(heading);
  ['before_review', 'after_refresh'].forEach(state => { const cell = document.createElement('td'); cell.textContent = `${report.metrics[state][key]}/${report.metrics[state].total}`; row.append(cell); }); tbody.append(row);
});
table.append(tbody); byId('metrics-table').append(table);

const nav = byId('navigation'); const toggle = document.querySelector('.nav-toggle');
function closeNav() { nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label', 'Open navigation'); }
toggle.addEventListener('click', () => { const open = toggle.getAttribute('aria-expanded') !== 'true'; toggle.setAttribute('aria-expanded', String(open)); toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation'); nav.classList.toggle('is-open', open); });
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeNav));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { closeNav(); toggle.focus(); } });
document.addEventListener('click', event => { if (!document.querySelector('.site-header').contains(event.target)) closeNav(); });

const storyMessages = ['A new source version is available.', 'The answer still cites the previous version.', 'Checks guide the review. The owner decides.'];
function showJourney(index) {
  document.querySelector('.journey-canvas').dataset.stage = String(index);
  all('[data-journey]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.journey) === index)));
  all('[data-story-stage]').forEach(stage => stage.classList.toggle('is-current', Number(stage.dataset.storyStage) === index));
  put('journey-status', storyMessages[index]);
}
all('[data-journey]').forEach(button => button.addEventListener('click', () => {
  const index = Number(button.dataset.journey); showJourney(index);
  if (window.matchMedia('(min-width: 701px)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelector(`[data-story-stage="${index}"]`).scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}));
put('journey-source', currentVersion); put('journey-answer', oldVersion); showJourney(0);
if ('IntersectionObserver' in window) {
  const sectionObserver = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) nav.querySelectorAll('a').forEach(link => {
      if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
    });
  }), { rootMargin: '-15% 0px -65% 0px' });
  all('main section[id]').forEach(section => sectionObserver.observe(section));
  const storyObserver = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) showJourney(Number(entry.target.dataset.storyStage));
  }), { rootMargin: '-25% 0px -45% 0px', threshold: 0 });
  all('[data-story-stage]').forEach(stage => storyObserver.observe(stage));
  const revealObserver = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('is-visible'); revealObserver.unobserve(entry.target); }
  }), { threshold: 0.06 });
  all('.section-heading,.experiment,.queue-grid,.queue-preview,.flow-grid,.evidence-grid,.about-grid').forEach(element => { element.classList.add('reveal'); revealObserver.observe(element); });
}
let scrollPending = false;
function updateScroll() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = max > 0 ? window.scrollY / max : 0;
  document.querySelector('.reading-progress span').style.transform = `scaleX(${ratio})`;
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) document.querySelector('.hero-artwork').style.setProperty('--art-shift', `${Math.min(60, window.scrollY * 0.08)}px`);
  scrollPending = false;
}
window.addEventListener('scroll', () => { if (!scrollPending) { scrollPending = true; window.requestAnimationFrame(updateScroll); } }, { passive: true });
window.addEventListener('resize', updateScroll);
render(); updateScroll(); document.body.dataset.ready = 'trust-v3';
