"""Publish the reviewed, non-promotional technical article once. Requires DEVTO_API_KEY."""
import json, os
from pathlib import Path
from urllib.request import Request, urlopen
key = os.environ['DEVTO_API_KEY']
body = Path(__file__).with_name('article.md').read_text()
title, content = body.split('\n', 1)
# Refuse a duplicate title rather than creating a second post on a rerun.
headers = {'api-key': key, 'Accept': 'application/vnd.forem.api-v1+json', 'User-Agent': 'CloudGPU-Technical-Publishing/1.0'}
with urlopen(Request('https://dev.to/api/articles/me/all?per_page=100', headers=headers), timeout=30) as r:
    existing = json.load(r)
if any(a.get('title') == title.removeprefix('# ') for a in existing):
    raise SystemExit('Article already exists; inspect it before updating or republishing.')
payload = {'article': {'title': title.removeprefix('# '), 'published': True, 'body_markdown': content.strip(), 'tags': ['ai', 'python', 'architecture', 'tutorial']}}
headers['Content-Type'] = 'application/json'
req = Request('https://dev.to/api/articles', headers=headers, data=json.dumps(payload).encode(), method='POST')
with urlopen(req, timeout=30) as r:
    result = json.load(r)
print(json.dumps({'id': result.get('id'), 'url': result.get('url'), 'published_at': result.get('published_at')}))
