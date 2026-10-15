import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from triage import queue
class TriageTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.payload=queue(); cls.items={x['policy_id']:x for x in cls.payload['items']}
 def test_all_answers_are_blocked_pending_security_review(self):
  self.assertEqual(self.payload['summary']['blocked_pending_approval'],12)
  self.assertTrue(all(x['review_state']=='pending_human_approval' for x in self.items.values()))
 def test_unsupported_claim_escalates(self):
  self.assertEqual(self.items['EXPORT-09']['decision'],'block_and_escalate')
  self.assertEqual(self.items['EXPORT-09']['priority'],'P0')
 def test_sso_change_requires_rewrite(self):
  self.assertEqual(self.items['AUTH-01']['decision'],'rewrite_and_review')
 def test_stable_encryption_requires_provenance_review(self):
  self.assertEqual(self.items['ENC-04']['decision'],'revalidate_provenance')
 def test_missing_citation_is_not_approved(self):
  self.assertEqual(self.items['BACK-08']['decision'],'repair_evidence_and_review')
 def test_queue_prioritizes_escalation(self):
  self.assertEqual(self.payload['items'][0]['priority'],'P0')
 def test_every_item_has_evidence_and_owner(self):
  self.assertTrue(all(i['evidence'] and i['owner'] and i['action'] for i in self.items.values()))
 def test_no_customer_publication_claim(self):
  self.assertTrue(all(x['publish_blocked'] for x in self.items.values()))
if __name__=='__main__':unittest.main()