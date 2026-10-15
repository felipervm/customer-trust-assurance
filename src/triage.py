"""Source-change impact analysis and safe publication triage on fictional fixtures.

This is a deterministic decision-support queue. It NEVER authorizes customer publication.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from evaluate import ROOT, load, run

OUT = ROOT / 'data' / 'review_queue.json'
OWNER_BY_TOPIC = {
    'sso':'Identity & Access', 'data_residency':'Privacy & Legal',
    'incident_notice':'Security Operations', 'encryption':'Security Engineering',
    'audit_logs':'Security Operations', 'subprocessor':'Privacy & Legal',
    'mfa':'Identity & Access', 'backups':'Infrastructure',
    'exports':'Product Security', 'penetration_tests':'Security Assurance',
    'data_deletion':'Privacy & Legal', 'access_reviews':'Identity & Access'
}


def classify(policy, case, current_version):
    old_value=policy['versions'][case['source_version']]['value']
    current_value=policy['versions'][current_version]['value']
    findings=case['evaluation']['findings']
    changed=old_value != current_value
    unsupported='answer_conflicts_with_current_policy' in findings and case['answer'] != policy['versions'][case['source_version']]['answer']
    if unsupported:
        reason='unsupported_claim'
        decision='block_and_escalate'
        priority='P0'
        work='Check the unsupported customer-facing claim against authoritative evidence before drafting a replacement.'
    elif changed:
        reason='policy_changed'
        decision='rewrite_and_review'
        priority='P1'
        work='Update the answer from the current approved policy, then obtain owner sign-off.'
    elif 'citation_missing_or_wrong' in findings:
        reason='missing_citation'
        decision='repair_evidence_and_review'
        priority='P1'
        work='Attach the current authoritative policy citation and request owner confirmation.'
    elif 'source_version_outdated' in findings:
        reason='stale_provenance_only'
        decision='revalidate_provenance'
        priority='P2'
        work='Verify the claim remains unchanged, refresh evidence version, and request owner confirmation.'
    else:
        reason='all_checks_pass'
        decision='ready_for_owner_approval'
        priority='P3'
        work='Request security owner approval before customer publication.'
    return dict(policy_id=case['policy_id'],topic=policy['topic'],question=case['question'],
                owner=OWNER_BY_TOPIC.get(policy['topic'],'Security Assurance'),
                source_version=case['source_version'],required_version=current_version,
                source_changed=changed,reason=reason,decision=decision,priority=priority,
                publish_blocked=True,action=work,
                evidence={'previous_claim':case['answer'], 'approved_current_text':case['current_answer'],
                          'cited_policy_id':case['citation'], 'findings':findings},
                review_state='pending_human_approval')


def queue():
    knowledge=load()
    report=run()
    current=report['metadata']['current_version']
    by_id={p['id']:p for p in knowledge['policies']}
    prior=[x for x in report['cases'] if x['phase']=='before_review']
    items=[classify(by_id[x['policy_id']],x,current) for x in prior]
    rank={'P0':0,'P1':1,'P2':2,'P3':3}
    items.sort(key=lambda x:(rank[x['priority']],x['policy_id']))
    counts=dict(sorted(Counter(x['reason'] for x in items).items()))
    priorities=dict(sorted(Counter(x['priority'] for x in items).items()))
    assert len(items)==len(by_id)==12
    assert all(x['publish_blocked'] for x in items)
    return {
      'metadata':{'title':'Assurance change-impact queue','scope':'Synthetic, deterministic exercise only',
                  'current_knowledge_version':current,'not_an_agent_benchmark':True,
                  'gate':'All outgoing claims require human security owner approval'},
      'summary':{'total_answers_reviewed':len(items),'blocked_pending_approval':len(items),
                 'by_reason':counts,'by_priority':priorities},'items':items}


def main():
    payload=queue()
    OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(payload['summary'],indent=2))

if __name__=='__main__':main()