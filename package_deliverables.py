"""Create an overlay archive and a self-contained portfolio review copy."""
from pathlib import Path
import base64
import json
import mimetypes
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'deliverables'
OUT.mkdir(exist_ok=True)
EXCLUDE = {
    'original-index.html', 'preview.html', 'insulin-infusion/index.html',
    'assets/ai-guest-speaker.jpg', 'assets/insulin-assistant.jpg',
}
files = [p for p in sorted(ROOT.rglob('*')) if p.is_file()
         and p.relative_to(ROOT).as_posix() not in EXCLUDE
         and '__pycache__' not in p.parts
         and 'tests/artifacts/' not in p.relative_to(ROOT).as_posix()]
archive = OUT / 'gurkan-camok-portfolio-revised.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, p.relative_to(ROOT).as_posix())
    if not (ROOT / '.nojekyll').is_file():
        z.writestr('.nojekyll', '')

assets = {'/' + p.relative_to(ROOT).as_posix():
          'data:' + mimetypes.guess_type(p.name)[0] + ';base64,' + base64.b64encode(p.read_bytes()).decode()
          for p in files if p.suffix in {'.jpg', '.png', '.pdf'}}
paths = ['index.html', 'evidence/index.html', 'profile/index.html', 'privacy/index.html']
paths += [p.relative_to(ROOT).as_posix() for p in ROOT.glob('projects/*/index.html')]
pages = {}
for name in paths:
    source = (ROOT / name).read_text()
    body = source.split('<body>', 1)[1].split('</body>', 1)[0]
    body = body.replace('href="/insulin-infusion/"', 'href="https://gurkancamok.github.io/insulin-infusion/" target="_blank" rel="noopener noreferrer"')
    path = '/' if name == 'index.html' else '/' + name[:-10]
    pages[path] = {'body': body, 'title': re.search(r'<title>(.*?)</title>', source).group(1)}

script = r"""
const pages=JSON.parse(document.getElementById('pages').textContent);
const assets=JSON.parse(document.getElementById('assets').textContent);
function closeMenu(restore=false){const b=document.querySelector('.menu-toggle');document.querySelector('.nav-links')?.classList.remove('open');b?.setAttribute('aria-expanded','false');if(restore)b?.focus();}
function render(path,fragment=''){const p=pages[path];if(!p)return;let body=p.body;for(const [src,data] of Object.entries(assets))body=body.split(src).join(data);document.getElementById('portfolio').innerHTML=body;document.title=p.title+' — Preview';initializeRecognitionGalleries();if(fragment){requestAnimationFrame(()=>document.getElementById(fragment)?.scrollIntoView());}else{window.scrollTo(0,0);}}
document.addEventListener('click',event=>{const button=event.target.closest('.menu-toggle');if(button){const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));document.getElementById('primary-navigation').classList.toggle('open',open);return;}const a=event.target.closest('a');if(!a){if(!event.target.closest('.nav-links'))closeMenu();return;}const href=a.getAttribute('href');if(!href||a.hasAttribute('download'))return;if(href.startsWith('#')){closeMenu();return;}if(href.startsWith('/')){const [path,fragment]=href.split('#');if(pages[path]){event.preventDefault();render(path,fragment||'');}}});
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeMenu(true);});
matchMedia('(min-width:781px)').addEventListener('change',()=>closeMenu());
render('/');
"""
preview = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1">'
           '<title>Gürkan Çamok — revised portfolio preview</title><style>'
           + (ROOT / 'assets/site.css').read_text() + '</style></head><body><div id="portfolio">'
           + '<p class="shell" style="padding-block:40px">Loading portfolio…</p></div>'
           + '<noscript><p class="shell">Enable JavaScript in your browser to view this interactive preview.</p></noscript>'
           + '<script id="pages" type="application/json">'
           + json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')
           + '</script><script id="assets" type="application/json">'
           + json.dumps(assets, ensure_ascii=False).replace('</', '<\\/')
           + '</script><script>' + (ROOT / 'assets/gallery.js').read_text() + '</script><script>' + script + '</script></body></html>')
(OUT / 'gurkan-camok-portfolio-preview.html').write_text(preview)
shutil.copy2(ROOT / 'downloads/gurkan-camok-professional-profile.pdf', OUT / 'gurkan-camok-professional-profile.pdf')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert 'insulin-infusion/index.html' not in z.namelist()
    removed_contact = '@'.join(['gurkan.camok', 'anadolusaglik.org']).encode()
    for name in z.namelist():
        if name.endswith(('.html', '.py', '.js', '.md', '.txt')):
            assert removed_contact not in z.read(name), name
print(f'Created and verified {len(files)+1}-file overlay archive and standalone preview.')
