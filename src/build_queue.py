"""Build both standalone reviewer handoff pages from the deterministic queue."""
import json
from triage import ROOT, queue


def render(payload):
    template=(ROOT/'site/queue-template.html').read_text(encoding='utf-8')
    replacements={
      '__PAYLOAD__':json.dumps(payload,separators=(',',':'),ensure_ascii=False).replace('<','\\u003c'),
      '__QUEUE_THEME__':(ROOT/'site/queue-theme.css').read_text(encoding='utf-8'),
      '__QUEUE_APP__':(ROOT/'site/queue-app.js').read_text(encoding='utf-8'),
    }
    for token,value in replacements.items():
        if template.count(token)!=1:
            raise ValueError(f'Expected one queue token: {token}')
        template=template.replace(token,value)
    return template


def main():
    rendered=render(queue())
    for path in (ROOT/'review-queue.html',ROOT/'site/review-queue.html'):
        path.write_bytes(rendered.encode('utf-8'))
    print('Built synthetic review-queue demo')

if __name__=='__main__':main()
