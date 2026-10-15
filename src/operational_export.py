"""Traceable review handoff for fictional policy changes; no automated approval."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
from triage import ROOT, queue
from evaluate import load

FIELDS = ['case_id','policy_id','topic','priority','reason','decision','owner','review_state','source_version','required_version','source_changed','source_sha256','next_action','publish_blocked']

def evidence_fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()

def build_handoff():
    payload=queue()
    knowledge=load()
    by_id={p['id']:p for p in knowledge['policies']}
    records=[]; lineage=[]
    for item in payload['items']:
        p=by_id[item['policy_id']]
        old=p['versions'][item['source_version']]
        current=p['versions'][item['required_version']]
        digest=evidence_fingerprint(current)
        case_id='REVIEW-'+item['policy_id']
        records.append({'case_id':case_id,'policy_id':item['policy_id'],'topic':item['topic'],
            'priority':item['priority'],'reason':item['reason'],'decision':item['decision'],
            'owner':item['owner'],'review_state':item['review_state'],
            'source_version':item['source_version'],'required_version':item['required_version'],
            'source_changed':str(item['source_changed']).lower(),'source_sha256':digest,
            'next_action':item['action'],'publish_blocked':str(item['publish_blocked']).lower()})
        lineage.append({'case_id':case_id,'policy_id':item['policy_id'],'question':item['question'],
            'prior_evidence':{'version':item['source_version'],'value':old['value'],'answer':old['answer'], 'fingerprint':evidence_fingerprint(old)},
            'current_evidence':{'version':item['required_version'],'value':current['value'],'answer':current['answer'],'fingerprint':digest},
            'prior_response':item['evidence']['previous_claim'],'citation_id':item['evidence']['cited_policy_id'],
            'evaluation_findings':item['evidence']['findings'],'proposed_action':item['decision'],
            'audit_note':'Automated triage recommendation only. A security owner must verify the underlying evidence and approve any external answer.'})
    return records,{'metadata':{'scope':'Synthetic assurance evidence lineage; not a real customer or Chainguard system',
         'publication_policy':'Human security owner review required for every case',
         'fingerprint':'SHA-256 of canonical JSON evidence record; integrity pointer only, not proof of authenticity'},
         'cases':lineage}

def main():
    records,lineage=build_handoff()
    folder=ROOT/'data';folder.mkdir(exist_ok=True)
    with (folder/'review_handoff.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(records)
    (folder/'evidence_lineage.json').write_text(json.dumps(lineage,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Exported {len(records)} fictional cases and source lineage records')

if __name__=='__main__':main()