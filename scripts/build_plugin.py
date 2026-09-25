#!/usr/bin/env python3
"""Build the distributable plugin from the canonical repository skill copy."""
import argparse
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def build(check=False):
    source = ROOT / 'skills/lesson-pair'
    dest = ROOT / 'plugins/lesson-pair'
    files = {str(p.relative_to(source)): p.read_bytes() for p in source.rglob('*')
             if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    expected = {dest / 'skills/lesson-pair' / path: value for path, value in files.items()}
    manifest = {'$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
                'name': 'lesson-pair', 'version': '0.2.0',
                'homepage': 'https://sjskoko.github.io/lesson-pair/',
                'repository': 'https://github.com/sjskoko/lesson-pair', 'license': 'MIT',
                'keywords': ['english-learning', 'video-learning', 'chatgpt', 'agent-skills', 'bring-your-own-ai'],
                'description': 'Explain a video you love in your own English. Guided practice, your own before/after, optional Notion.',
                'homepage': 'https://sjskoko.github.io/lesson-pair/', 'repository': 'https://github.com/sjskoko/lesson-pair',
                'license': 'MIT', 'keywords': ['english-learning', 'video-learning', 'chatgpt', 'agent-skills', 'bring-your-own-ai'],
                'extensions': {'com.openai': {'interface': {
                    'displayName': 'LessonPair', 'shortDescription': 'One video. Your AI. Your own English.',
                    'longDescription': 'Guided English practice from a video: try, practice what you need, retry, and compare your own answers. Notion is optional.',
                    'category': 'Productivity', 'websiteURL': 'https://sjskoko.github.io/lesson-pair/',
                    'privacyPolicyURL': 'https://github.com/sjskoko/lesson-pair/blob/main/SECURITY.md',
                    'defaultPrompt': ['Help me explain this English video in my own words, one question at a time.']}}}}
    expected[dest / 'plugin.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    marketplace = {'name': 'lesson-pair-marketplace', 'interface': {'displayName': 'LessonPair'},
                   'plugins': [{'name': 'lesson-pair', 'source': {'source': 'local', 'path': './plugins/lesson-pair'},
                                'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Productivity'}]}
    expected[ROOT / '.agents/plugins/marketplace.json'] = (json.dumps(marketplace, indent=2) + '\n').encode()
    stale = [str(p.relative_to(ROOT)) for p, data in expected.items() if not p.exists() or p.read_bytes() != data]
    extras = [p for p in dest.rglob('*') if p.is_file() and p not in expected and '__pycache__' not in p.parts]
    if check:
        if stale or extras:
            raise SystemExit('Rebuild plugin: ' + ', '.join(stale + [str(p.relative_to(ROOT)) for p in extras]))
    else:
        for p in extras: p.unlink()
        for p, data in expected.items():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
    print(f'Plugin {"verified" if check else "built"}: {len(expected)} files; one canonical skill source.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)
