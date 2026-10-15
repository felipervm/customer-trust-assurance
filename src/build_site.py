"""Embed the exact evaluated fixture dataset in both static HTML entrypoints."""
import base64
import json
from pathlib import Path
from evaluate import ROOT, build
from evaluate import load
from triage import queue

def json_script(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')

def render(payload):
    template=(ROOT/'site'/'template.html').read_text(encoding='utf-8')
    font='data:font/woff2;base64,'+base64.b64encode((ROOT/'site/assets/fonts/manrope-latin.woff2').read_bytes()).decode('ascii')
    font_css="@font-face{font-family:Manrope;font-style:normal;font-weight:400 700;font-display:swap;src:url("+font+") format('woff2')}"
    replacements={
      '__EVALUATION_PAYLOAD__':json_script(payload),
      '__QUEUE_PAYLOAD__':json_script(queue()),
      '__KNOWLEDGE_PAYLOAD__':json_script(load()),
      '__STYLES__':font_css+(ROOT/'site'/'styles.css').read_text(encoding='utf-8'),
      '__APP__':(ROOT/'site'/'app.js').read_text(encoding='utf-8'),
      '__PORTRAIT__':'data:image/jpeg;base64,'+base64.b64encode((ROOT/'site'/'assets'/'felipe-mattos.jpg').read_bytes()).decode('ascii'),
      '__HERO_ART__':'data:image/jpeg;base64,'+base64.b64encode((ROOT/'site'/'assets'/'trust-records.jpg').read_bytes()).decode('ascii'),
    }
    for token,value in replacements.items():
        if template.count(token)!=1:
            raise ValueError(f'Expected one presentation token: {token}')
        template=template.replace(token,value)
    return template

def main():
    payload=build()
    rendered=render(payload)
    for target in (ROOT/'site'/'index.html',ROOT/'index.html'):
        target.write_bytes(rendered.encode('utf-8'))
    print('Generated both published HTML entrypoints from evaluated data.')

if __name__=='__main__':main()
