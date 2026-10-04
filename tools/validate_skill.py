#!/usr/bin/env python3
"""Validate this repository's skill structure with Python's standard library."""
import ast
from pathlib import Path
import re
import sys
from urllib.parse import unquote


def validate(root):
    root = Path(root).resolve()
    errors = []
    entry = root / 'SKILL.md'
    if not entry.is_file():
        return ['SKILL.md is missing']
    text = entry.read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        errors.append('Missing frontmatter')
    else:
        fields = dict(re.findall(r'^(name|description):\s*(.+)$', match[1], re.M))
        if fields.get('name') != 'github-agent':
            errors.append('Unexpected or missing skill name')
        if not fields.get('description'):
            errors.append('Description is missing')
        if len(match[1].splitlines()) != 2:
            errors.append('Expected only single-line name and description fields')
    if len(text.splitlines()) > 500:
        errors.append('Entry exceeds 500 lines')
    references = sorted((root / 'references').glob('*.md'))
    for ref in references:
        if 'references/' + ref.name not in text:
            errors.append('Unrouted reference: ' + ref.name)
        if len(ref.read_text(encoding='utf-8').splitlines()) > 100:
            if '内容：' not in ref.read_text(encoding='utf-8')[:1200]:
                errors.append('Long reference needs an outline: ' + ref.name)
    for path in root.rglob('*.md'):
        content = path.read_text(encoding='utf-8')
        fences = re.findall(r'^```', content, re.M)
        if len(fences) % 2:
            errors.append('Unclosed code fence: ' + str(path.relative_to(root)))
        # Check local Markdown links, ignoring code examples and external URLs.
        prose = re.sub(r'^```.*?^```[^\n]*', '', content, flags=re.M | re.S)
        for target in re.findall(r'\]\(([^)\s]+)\)', prose):
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target) or target.startswith('#'):
                continue
            local = unquote(target.split('#', 1)[0])
            if not (path.parent / local).exists():
                errors.append(f'Broken link in {path.name}: {target}')
    for path in (root / 'scripts').glob('*.py'):
        try:
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        except SyntaxError as exc:
            errors.append(str(exc))
    metadata = root / 'agents' / 'openai.yaml'
    if not metadata.is_file() or '$github-agent' not in metadata.read_text(encoding='utf-8'):
        errors.append('Missing agent metadata or default prompt')
    return errors


if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'github-agent'
    errors = validate(root)
    for error in errors:
        print('ERROR:', error)
    if not errors:
        print('Skill structure, routing, local links, metadata and Python syntax passed.')
    sys.exit(bool(errors))
