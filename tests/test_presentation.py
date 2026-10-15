"""Publishing checks supplement the assurance, triage and handoff tests."""
import base64,json,re,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from build_site import render,json_script
from build_queue import render as render_queue
from evaluate import run,load
from triage import queue

class PresentationTests(unittest.TestCase):
    def test_standalone_pages_rebuild_exactly(self):
        for filename,expected in [('index.html',render(run())),('review-queue.html',render_queue(queue()))]:
            expected=expected.encode('utf-8')
            self.assertEqual((ROOT/filename).read_bytes(),expected)
            self.assertEqual((ROOT/'site'/filename).read_bytes(),expected)
    def test_embedded_data_matches_authoritative_models(self):
        html=(ROOT/'index.html').read_text(encoding='utf-8')
        for script_id,expected in [('case-data',run()),('queue-data',queue()),('knowledge-data',load())]:
            match=re.search(r'<script type="application/json" id="'+script_id+r'">(.*?)</script>',html,re.S)
            self.assertIsNotNone(match)
            self.assertEqual(json.loads(match.group(1)),expected)
        image=re.search(r'src="data:image/jpeg;base64,([^"]+)"',html)
        self.assertIsNotNone(image)
        self.assertEqual(base64.b64decode(image.group(1)),(ROOT/'site/assets/felipe-mattos.jpg').read_bytes())
    def test_script_payload_cannot_terminate_its_container(self):
        value={'answer':'</script><script>alert(1)</script>'}
        encoded=json_script(value)
        self.assertNotIn('<',encoded)
        self.assertEqual(json.loads(encoded),value)
    def test_link_targets_and_ids_are_valid(self):
        for filename in ['index.html','review-queue.html']:
            html=(ROOT/filename).read_text(encoding='utf-8')
            ids=re.findall(r'\bid="([^"]+)"',html)
            self.assertEqual(len(ids),len(set(ids)))
            for href in re.findall(r'href="([^"]+)"',html):
                if href.startswith('#'):self.assertIn(href[1:],ids)
                elif href.startswith('https://github.com/felipervm/customer-trust-assurance/blob/main/'):
                    self.assertTrue((ROOT/href.split('/blob/main/')[1]).is_file(),href)
                elif not href.startswith('http'):
                    self.assertTrue((ROOT/href.split('?')[0]).exists(),href)

if __name__=='__main__':unittest.main()
