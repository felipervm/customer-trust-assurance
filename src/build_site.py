"""Embed the exact evaluated fixture dataset in both static HTML entrypoints."""
import json
from pathlib import Path
from evaluate import ROOT, build

def main():
    payload=build()
    template=(ROOT/'site'/'template.html').read_text(encoding='utf-8')
    inline=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    rendered=template.replace('__EVALUATION_PAYLOAD__',inline)
    assert '__EVALUATION_PAYLOAD__' not in rendered
    for target in (ROOT/'site'/'index.html',ROOT/'index.html'):
        target.write_text(rendered,encoding='utf-8')
    print('Generated both published HTML entrypoints from evaluated data.')

if __name__=='__main__':main()