import csv
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from operational_export import build_handoff, evidence_fingerprint, main, ROOT
class OperationalHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records,cls.lineage=build_handoff()
    def test_all_items_have_unique_case_ids(self):
        self.assertEqual(len(self.records),12)
        self.assertEqual(len({x['case_id'] for x in self.records}),12)
    def test_all_records_blocked(self):
        self.assertTrue(all(r['publish_blocked']=='true' for r in self.records))
    def test_lineage_links_are_complete(self):
        self.assertEqual({x['case_id'] for x in self.records},{x['case_id'] for x in self.lineage['cases']})
    def test_fingerprints_stable_and_sensitive(self):
        self.assertEqual(evidence_fingerprint({'a':1}), evidence_fingerprint({'a':1}))
        self.assertNotEqual(evidence_fingerprint({'a':1}),evidence_fingerprint({'a':2}))
    def test_unsupported_response_preserved_in_audit(self):
        case=next(x for x in self.lineage['cases'] if x['policy_id']=='EXPORT-09')
        self.assertIn('answer_conflicts_with_current_policy',case['evaluation_findings'])
        self.assertEqual(case['proposed_action'],'block_and_escalate')
    def test_no_authenticity_claim_from_hash(self):
        self.assertIn('not proof of authenticity',self.lineage['metadata']['fingerprint'])
    def test_export_matches_data(self):
        main()
        with (ROOT/'data'/'review_handoff.csv').open(newline='',encoding='utf-8') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(rows,self.records)
if __name__=='__main__':unittest.main()