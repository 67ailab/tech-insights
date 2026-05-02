#!/usr/bin/env python3
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

DATE = '2026-05-01'
OUT = Path('/home/james/.openclaw/workspace/tech-insights/tmp_2026-05-01_data.json')

HN_KEYWORDS = [
    'ai', 'agent', 'agents', 'agentic', 'llm', 'gpt', 'claude', 'openai', 'anthropic',
    'multimodal', 'reasoning', 'alignment', 'copilot', 'prompt api', 'coding agent',
    'language model', 'language models'
]
HF_KEYWORDS = [
    'agent', 'agents', 'agentic', 'llm', 'language model', 'multimodal', 'benchmark',
    'interactive', 'productivity', 'scientist', 'research artifacts', 'terminal', 'web'
]


def keyword_match(text: str, keywords) -> bool:
    text = text.lower()
    for kw in keywords:
        if ' ' in kw:
            if kw in text:
                return True
        else:
            if re.search(r'(?<![a-z])' + re.escape(kw) + r'(?![a-z])', text):
                return True
    return False


def fetch_text(url: str) -> str:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def fetch_json(url: str):
    return json.loads(fetch_text(url))


# Hacker News top stories
hn_ids = fetch_json('https://hacker-news.firebaseio.com/v0/topstories.json')
hn_items = []
for item_id in hn_ids[:120]:
    try:
        item = fetch_json(f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json')
    except Exception:
        continue
    if not item or item.get('type') != 'story':
        continue
    title = item.get('title') or ''
    text = re.sub('<[^>]+>', ' ', item.get('text') or '')
    blob = (title + ' ' + text).lower()
    if item.get('score', 0) >= 100 and keyword_match(blob, HN_KEYWORDS):
        hn_items.append({
            'id': item_id,
            'title': title,
            'score': item.get('score', 0),
            'url': item.get('url') or f'https://news.ycombinator.com/item?id={item_id}',
            'hn_url': f'https://news.ycombinator.com/item?id={item_id}',
            'by': item.get('by'),
            'time': item.get('time'),
            'text': ' '.join(text.split()),
        })

hn_items.sort(key=lambda x: (-x['score'], -(x.get('time') or 0)))

# Hugging Face daily papers page
html = fetch_text('https://huggingface.co/papers')
entries = []
seen = set()
for m in re.finditer(r'/papers/(\d{4}\.\d{5})', html):
    pid = m.group(1)
    if pid in seen:
        continue
    seen.add(pid)
    chunk = html[m.start():m.start() + 900]
    vote_match = re.search(r'\[(\d+)\]\(/login\?next=%2Fpapers%2F' + re.escape(pid).replace('\\', '%') + r'\)', chunk)
    title_match = re.search(r'### \[(.*?)\]\(/papers/' + re.escape(pid) + r'\)', chunk, re.S)
    if not title_match:
        continue
    title = ' '.join(title_match.group(1).split())
    votes = int(vote_match.group(1)) if vote_match else 0
    if keyword_match(title.lower(), HF_KEYWORDS):
        entries.append({
            'id': pid,
            'title': title,
            'votes': votes,
            'url': f'https://huggingface.co/papers/{pid}'
        })

entries.sort(key=lambda x: (-x['votes'], x['id']))

OUT.write_text(json.dumps({'date': DATE, 'hn': hn_items[:8], 'hf': entries[:8]}, indent=2), encoding='utf-8')
print(str(OUT))
print(json.dumps({'hn': hn_items[:8], 'hf': entries[:8]}, indent=2))
