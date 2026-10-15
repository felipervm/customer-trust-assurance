"""Reproducible, offline evaluation of *simulated* questionnaire-agent responses.

No LLM API, invented accuracy claims, or real security attestations are involved.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data' / 'knowledge.json'
REPORT = ROOT / 'data' / 'evaluation.json'


def load():
    return json.loads(SOURCE.read_text(encoding='utf-8'))


def simulate_response(policy, *, agent_version, missing_citation=False, unsupported=False):
    """A controlled response fixture mimicking an assistant with a pinned policy index.

    This is NOT a generative AI invocation or a model benchmark.
    """
    record = policy['versions'][agent_version]
    if unsupported:
        return {'answer': 'This vendor is certified to ISO 27001.', 'claim': 'iso_certified', 'citation': policy['id'], 'source_version': agent_version}
    return {'answer': record['answer'], 'claim': record['value'], 'citation': None if missing_citation else policy['id'], 'source_version': agent_version}


def evaluate_response(policy, response, current_version):
    current = policy['versions'][current_version]
    accurate = response['claim'] == current['value']
    cited = response['citation'] == policy['id']
    current_source = response['source_version'] == current_version
    findings = []
    if not accurate:
        findings.append('answer_conflicts_with_current_policy')
    if not cited:
        findings.append('citation_missing_or_wrong')
    if not current_source:
        findings.append('source_version_outdated')
    return {'accurate': accurate, 'cited': cited, 'current_source': current_source,
            'publishable': accurate and cited and current_source, 'findings': findings}


def summarize(cases):
    count = len(cases)
    return {'total': count,
            'accurate': sum(c['evaluation']['accurate'] for c in cases),
            'cited': sum(c['evaluation']['cited'] for c in cases),
            'current_source': sum(c['evaluation']['current_source'] for c in cases),
            'publishable': sum(c['evaluation']['publishable'] for c in cases),
            'review_required': sum(not c['evaluation']['publishable'] for c in cases)}


def run():
    data = load()
    old, current = (v['id'] for v in data['versions'])
    cases = []
    for policy in data['policies']:
        # Baseline uses old version, with one additional missing citation and one hallucination fixture.
        for phase, version in [('before_review', old), ('after_refresh', current)]:
            response = simulate_response(policy, agent_version=version,
                missing_citation=(phase == 'before_review' and policy['id'] == 'BACK-08'),
                unsupported=(phase == 'before_review' and policy['id'] == 'EXPORT-09'))
            evaluation = evaluate_response(policy, response, current)
            cases.append({'phase':phase, 'policy_id':policy['id'], 'topic':policy['topic'],
                'question':policy['question'], 'current_answer':policy['versions'][current]['answer'],
                'answer':response['answer'], 'source_version':response['source_version'],
                'citation':response['citation'], 'evaluation':evaluation})
    before = [c for c in cases if c['phase']=='before_review']
    after = [c for c in cases if c['phase']=='after_refresh']
    changed = [p['id'] for p in data['policies'] if p['versions'][old]['value'] != p['versions'][current]['value']]
    payload = {'metadata':{'project':'Can We Still Trust This Answer?', 'vendor':data['vendor'],
        'data':'Entirely fictional; rules-based fixture simulation, NOT a live LLM benchmark',
        'old_version':old,'current_version':current},
        'change_log':{'changed_policies':changed,'unchanged_policies':len(data['policies'])-len(changed)},
        'metrics':{'before_review':summarize(before),'after_refresh':summarize(after)},
        'cases': cases}
    return payload


def build():
    result = run()
    REPORT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    assert result['metrics']['after_refresh']['publishable'] == 12
    assert result['metrics']['before_review']['publishable'] < 12
    print(json.dumps({'change_log':result['change_log'],'metrics':result['metrics']},indent=2))
    return result


if __name__ == '__main__':
    build()