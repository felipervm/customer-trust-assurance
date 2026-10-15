import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from evaluate import load,run,simulate_response,evaluate_response

class AssuranceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load();cls.r=run();cls.p=cls.data['policies']
    def test_synthetic_scope(self):
        self.assertIn('fictional',self.r['metadata']['data'].lower())
    def test_twelve_unique_policy_keys(self):
        self.assertEqual(len({p['id'] for p in self.p}),12)
    def test_six_policy_changes(self):
        self.assertEqual(len(self.r['change_log']['changed_policies']),6)
    def test_same_fixtures_each_phase(self):
        self.assertEqual(self.r['metrics']['before_review']['total'],12)
        self.assertEqual(self.r['metrics']['after_refresh']['total'],12)
    def test_old_answer_conflict(self):
        p=self.p[0]
        r=simulate_response(p,agent_version='2026-01')
        self.assertFalse(evaluate_response(p,r,'2026-09')['accurate'])
    def test_unchanged_answer_can_be_true_but_outdated(self):
        p=next(p for p in self.p if p['id']=='ENC-04')
        e=evaluate_response(p,simulate_response(p,agent_version='2026-01'),'2026-09')
        self.assertTrue(e['accurate']);self.assertFalse(e['publishable'])
    def test_missing_citation_is_flagged(self):
        p=self.p[7]
        e=evaluate_response(p,simulate_response(p,agent_version='2026-09',missing_citation=True),'2026-09')
        self.assertIn('citation_missing_or_wrong',e['findings'])
    def test_unsupported_claim_is_flagged(self):
        p=self.p[8]
        e=evaluate_response(p,simulate_response(p,agent_version='2026-09',unsupported=True),'2026-09')
        self.assertIn('answer_conflicts_with_current_policy',e['findings'])
    def test_post_refresh_all_pass(self):
        self.assertEqual(self.r['metrics']['after_refresh']['publishable'],12)
    def test_review_queue_exact(self):
        self.assertEqual(self.r['metrics']['before_review']['review_required'],12)
    def test_count_factual_accurate(self):
        self.assertEqual(self.r['metrics']['before_review']['accurate'],5)
    def test_citation_count(self):
        self.assertEqual(self.r['metrics']['before_review']['cited'],11)

if __name__=='__main__':unittest.main()