"""Check generated portfolio structure, assets and local link targets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / 'index.html', ROOT / '404.html'] + list(ROOT.glob('projects/*/index.html')) + [ROOT / x / 'index.html' for x in ['evidence', 'profile', 'privacy']]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags = []; self.ids = []; self.links = []; self.images = []; self.meta = {}; self.canonical = []; self.title = ''; self.schema = []; self.active = None
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); self.tags.append(tag)
        if a.get('id'): self.ids.append(a['id'])
        if tag == 'a' and a.get('href'): self.links.append(a)
        if tag == 'img': self.images.append(a)
        if tag == 'meta': self.meta[a.get('name', a.get('property', ''))] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical.append(a['href'])
        if tag == 'title': self.active = 'title'
        if tag == 'script' and a.get('type') == 'application/ld+json': self.active = 'schema'
    def handle_endtag(self, tag):
        if tag in ['title', 'script']: self.active = None
    def handle_data(self, data):
        if self.active == 'title': self.title += data
        elif self.active == 'schema': self.schema.append(json.loads(data))

pages = {p: Page(p.read_text()) for p in FILES}
errors = []; local_count = 0; image_count = 0
def check(ok, message):
    if not ok: errors.append(message)

for p, page in pages.items():
    label = str(p.relative_to(ROOT))
    check(page.tags.count('h1') == 1, f'{label}: one h1')
    check(page.tags.count('main') == 1, f'{label}: one main landmark')
    check(len(page.ids) == len(set(page.ids)), f'{label}: duplicate ids')
    check(bool(page.meta.get('description')), f'{label}: missing description')
    check(len(page.canonical) == 1, f'{label}: canonical')
    check(bool(page.schema), f'{label}: structured data')
    for a in page.links:
        u = urlsplit(a['href'])
        if a.get('target') == '_blank': check({'noopener','noreferrer'}.issubset(set(a.get('rel','').split())), f'{label}: unsafe external link')
        if u.scheme or u.netloc: continue
        target = (ROOT / unquote(u.path).lstrip('/')) if u.path.startswith('/') else p.parent / unquote(u.path)
        if not u.path: target = p
        if target.is_dir(): target = target / 'index.html'
        check(target.is_file(), f'{label}: missing link {a["href"]}'); local_count += 1
        if u.fragment and target.is_file():
            parsed = pages.get(target) or Page(target.read_text())
            check(unquote(u.fragment) in parsed.ids, f'{label}: missing anchor {a["href"]}')
    for img in page.images:
        check(bool(img.get('alt')), f'{label}: image alt')
        check((ROOT / img['src'].lstrip('/')).is_file(), f'{label}: missing image {img["src"]}')
        check(bool(img.get('width') and img.get('height')), f'{label}: intrinsic image size')
        image_count += 1
    for src in ['/assets/site.css', '/assets/site.js', '/assets/favicon.svg', '/assets/favicon.png', '/assets/apple-touch-icon.png', '/assets/social-card.png']:
        check((ROOT / src.lstrip('/')).is_file(), f'{label}: missing {src}')

for key, values in [('title',[p.title for p in pages.values()]), ('description',[p.meta['description'] for p in pages.values()]), ('canonical',[p.canonical[0] for p in pages.values()])]:
    check(len(values) == len(set(values)), f'Duplicate {key}')
ET.parse(ROOT / 'sitemap.xml')
check('noindex' in pages[ROOT / '404.html'].meta['robots'], '404 must be noindex')
legacy = ROOT / 'insulin-infusion-calculator-digital-health-tools-icu-clinical-support-app-diabetes-care-app/index.html'
check('0;url=/insulin-infusion/' in legacy.read_text(), 'Legacy application redirect')
check((ROOT / 'downloads/gurkan-camok-professional-profile.pdf').read_bytes().startswith(b'%PDF'), 'PDF signature')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} portfolio pages, {local_count} local links, {image_count} images, unique metadata, schema, sitemap, PDF and legacy redirect.')
