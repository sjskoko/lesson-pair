#!/usr/bin/env python3
"""Offline lesson formatter and focused Notion-table lint. Python 3.10+, stdlib only."""
import argparse
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def rich(value):
    """Escape user text, not structural Notion tags."""
    value = str(value)
    value = re.sub(r'([\\*~`$\[\]<>{}|^])', r'\\\1', value)
    return value.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '<br>')


def table(headers, rows):
    if not headers or any(len(row) != len(headers) for row in rows):
        raise ValueError('Table rows must have the same width as the header.')
    lines = ['<table header-row="true">']
    for row in [headers, *rows]:
        lines.append('<tr>')
        lines.extend('<td>' + rich(cell) + '</td>' for cell in row)
        lines.append('</tr>')
    return '\n'.join([*lines, '</table>'])


def raw_toggle(label, raw):
    if not isinstance(raw, str):
        raise ValueError('Original material must be a string.')
    fence = '`' * max(3, 1 + max((len(x) for x in re.findall(r'`+', raw)), default=0))
    # The archived JSON is the byte-faithful source; rendering keeps visible text.
    body = fence + 'text\n' + raw + '\n' + fence
    return '<details>\n<summary>' + rich(label) + '</summary>\n' + '\n'.join('\t' + x for x in body.split('\n')) + '\n</details>'


def validate(data):
    if not isinstance(data, dict):
        raise ValueError('The input must be a JSON object.')
    if not isinstance(data.get('topic'), str) or not data['topic'].strip():
        raise ValueError('topic must be a nonempty string.')
    session = data.get('session')
    if session is not None and (type(session) is not int or session < 1):
        raise ValueError('session must be a positive integer or null.')
    for field in ('lesson_date', 'organized_date'):
        value = data.get(field)
        if value is not None:
            if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                raise ValueError(field + ' must be YYYY-MM-DD or null.')
            dt.date.fromisoformat(value)
    for field in ('learner_original', 'teacher_trace', 'teacher_notes', 'summary', 'corrected_text'):
        if field in data and not isinstance(data[field], str):
            raise ValueError(field + ' must be a string.')
    if data.get('video_url'):
        parsed = urlparse(data['video_url'])
        if parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError('video_url must be a public HTTP(S) link without credentials.')
    list_fields = {
        'corrections': ('original', 'corrected', 'reason', 'source'),
        'grammar': ('chunk', 'rule', 'example'),
        'segments': ('title', 'original', 'translation', 'grammar'),
        'exercises': ('question', 'answer'),
    }
    for name, fields in list_fields.items():
        rows = data.get(name, [])
        if not isinstance(rows, list):
            raise ValueError(name + ' must be an array.')
        for row in rows:
            if not isinstance(row, dict) or any(not isinstance(row.get(k), str) for k in fields):
                raise ValueError(name + ' entries require string fields: ' + ', '.join(fields))
    for name in ('chunks', 'questions'):
        if not isinstance(data.get(name, []), list) or any(not isinstance(x, str) for x in data.get(name, [])):
            raise ValueError(name + ' must contain strings.')
    return data


def render(data):
    validate(data)
    label = 'Session ' + (f"{data['session']:02d}" if data.get('session') else '—')
    title = label + ' · ' + data['topic']
    dates = '수업일: ' + (data.get('lesson_date') or '미확인') + ' / 정리일: ' + (data.get('organized_date') or '미기록')
    session = '\n'.join([
        '# ' + rich(title), dates, '',
        '**상태:** 로컬 초안. Notion에는 아직 저장되지 않았습니다.',
        '## 한 수업, 두 자료',
        '[① 영상 예습 자료](01-preparation.notion.md)',
        '[② 수업·복습 기록](02-review.notion.md)',
        'Notion 저장 후 실제 두 페이지 URL과 상호 멘션을 연결합니다.',
        '## 완료 기준', '- [ ] 원본과 교정 출처를 확인했다.',
        '- [ ] 자료를 가리고 재작문했다.', '- [ ] 다음 복습일을 정했다.',
    ])
    prep = ['# ① 영상 예습 자료 · ' + rich(title), dates,
            '**짝 자료:** Notion 저장 후 수업·복습 기록을 연결합니다.']
    if data.get('video_url'):
        prep.append('영상: ' + rich(data['video_url']))
    prep.extend(['## 핵심 요약', rich(data.get('summary', '아직 작성하지 않았습니다.'))])
    if not data.get('segments'):
        prep.append('원문이 제공되지 않았습니다. 영상 제목만으로 자막을 생성하지 않습니다.')
    for segment in data.get('segments', []):
        prep.extend(['## ' + rich(segment['title']), raw_toggle('영어 원문', segment['original']),
                     '### 해석', rich(segment['translation']),
                     '<callout icon="📝" color="gray_bg">\n\t' + rich(segment['grammar']) + '\n</callout>'])
    prep.extend(['## 사용할 표현', *('- ' + rich(x) for x in data.get('chunks', [])),
                 '- [ ] 영상을 확인했다.', '- [ ] 표현으로 내 문장을 만들었다.'])
    review = ['# ② 수업·복습 기록 · ' + rich(title), dates,
              '**짝 자료:** Notion 저장 후 영상 예습 자료를 연결합니다.',
              '**작문 목표:** 5분 / 실제 소요 시간: 미기록', '## 원본 보존']
    for key, label in [('learner_original', '내 즉석 작문 원본'), ('teacher_trace', '수업 중 교정 흔적'), ('teacher_notes', '선생님 메모 원본')]:
        if key in data:
            review.append(raw_toggle(label, data[key]))
    review.extend(['## 문장별 교정', table(['원문', '교정안', '이유', '출처'],
                   [[row[k] for k in ('original', 'corrected', 'reason', 'source')] for row in data.get('corrections', [])])])
    if data.get('corrected_text'):
        review.extend(['## 정리된 교정본', '**출처:** ' + rich(data.get('corrected_text_source', 'AI 보완안 — 확인 필요')), rich(data['corrected_text'])])
    review.extend(['## 문법·표현', table(['표현', '규칙·예외', '예문'],
                   [[row[k] for k in ('chunk', 'rule', 'example')] for row in data.get('grammar', [])]),
                   '## 암기 문장', *('- ' + rich(x) for x in data.get('chunks', [])), '## 가리고 풀기'])
    for i, exercise in enumerate(data.get('exercises', []), 1):
        review.append(str(i) + '. ' + rich(exercise['question']))
    answers = '\n'.join(str(i) + '. ' + x['answer'] for i, x in enumerate(data.get('exercises', []), 1))
    if answers:
        review.append(raw_toggle('정답 예시', answers))
    review.extend(['## 내 재작문', '자료를 가리고 다시 작성합니다. 아직 작성하지 않았습니다.',
                   '- [ ] 핵심 표현을 사용했다.', '- [ ] 모든 문장을 끝까지 완성했다.',
                   '## 다음 수업 질문', *('- [ ] ' + rich(x) for x in data.get('questions', []))])
    return {'session.md': session + '\n', '01-preparation.notion.md': '\n'.join(prep) + '\n',
            '02-review.notion.md': '\n'.join(review) + '\n'}


def lint(text):
    """Detect the observed table failure; not a complete Notion Markdown parser."""
    errors, widths, row_width = [], [], None
    in_table = False
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        marker = re.match(r'^(`{3,}|~{3,})', stripped)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and stripped == run:
                fence = None
            continue
        if fence:
            continue
        if re.match(r'^\s*\\<(?:/?table|/?tr|/?td)\b', line):
            errors.append(f'line {number}: escaped table tags render as text')
        if re.match(r'^\s*&(?:lt|#60|#x3c);/?(?:table|tr|td)\b', line, re.I):
            errors.append(f'line {number}: HTML-encoded table tags render as text')
        if re.search(r'<table\b[^>]*>.*<(?:tr|td)\b', line):
            errors.append(f'line {number}: table structure must span separate lines')
        if stripped.startswith('<table ') or stripped == '<table>':
            if in_table:
                errors.append(f'line {number}: nested/unclosed table')
            in_table, widths = True, []
        elif stripped == '<tr>':
            if not in_table or row_width is not None:
                errors.append(f'line {number}: misplaced row')
            row_width = 0
        elif stripped.startswith('<td>'):
            if row_width is None or not stripped.endswith('</td>'):
                errors.append(f'line {number}: misplaced/unclosed cell')
            else:
                row_width += 1
        elif stripped == '</tr>':
            if row_width is None:
                errors.append(f'line {number}: stray closing row')
            else:
                widths.append(row_width)
            row_width = None
        elif stripped == '</table>':
            if not in_table:
                errors.append(f'line {number}: stray closing table')
            elif row_width is not None or not widths or len(set(widths)) != 1 or widths[0] == 0:
                errors.append(f'line {number}: table rows have invalid widths')
            in_table = False
    if in_table or row_width is not None:
        errors.append('unclosed table or row')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    build = sub.add_parser('render', help='Render supplied JSON into local drafts; no network calls')
    build.add_argument('input', type=Path)
    build.add_argument('--out', type=Path, required=True)
    check = sub.add_parser('check', help='Check a Markdown file for broken table structure')
    check.add_argument('path', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'check':
            errors = lint(args.path.read_text(encoding='utf-8'))
            for error in errors:
                print(error)
            if errors:
                return 1
            print('OK: no known table-format errors')
            return 0
        raw = args.input.read_bytes()
        data = json.loads(raw)
        files = render(data)
        for name, content in files.items():
            errors = lint(content)
            if errors:
                raise ValueError(name + ': ' + '; '.join(errors))
        args.out.mkdir(parents=True, exist_ok=True)
        for name in [*files, 'source.json']:
            if (args.out / name).exists():
                raise ValueError('Refusing to overwrite ' + str(args.out / name))
        for name, content in files.items():
            (args.out / name).write_text(content, encoding='utf-8')
        (args.out / 'source.json').write_bytes(raw)
        print(f'Created {len(files)} local drafts and preserved source.json. Not uploaded to Notion.')
        return 0
    except (ValueError, TypeError, OSError) as exc:
        parser.exit(2, f'Error: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
