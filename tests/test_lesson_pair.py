import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/lesson-pair/scripts/lesson_pair.py'
spec = importlib.util.spec_from_file_location('lesson_pair', SCRIPT)
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)


class LessonPairTests(unittest.TestCase):
    def sample(self):
        return json.loads((ROOT / 'examples/lesson.synthetic.json').read_text())

    def test_original_and_trace_are_retained(self):
        data = self.sample()
        output = lp.render(data)['02-review.notion.md']
        self.assertIn(data['learner_original'], output)
        self.assertIn(data['teacher_trace'], output)

    def test_lesson_date_not_replaced_by_organization_date(self):
        out = lp.render(self.sample())['session.md']
        self.assertIn('수업일: 2030-01-15 / 정리일: 2030-01-16', out)

    def test_absent_dates_remain_unknown(self):
        out = lp.render({'topic': 'Sample'})['session.md']
        self.assertIn('수업일: 미확인 / 정리일: 미기록', out)

    def test_ambiguous_date_rejected(self):
        with self.assertRaises(ValueError):
            lp.render({'topic': 'Sample', 'lesson_date': '01/02/2030'})

    def test_bool_is_not_session_number(self):
        with self.assertRaises(ValueError):
            lp.render({'topic': 'Sample', 'session': True})

    def test_no_invented_transcript(self):
        self.assertIn('원문이 제공되지 않았습니다', lp.render({'topic': 'Sample'})['01-preparation.notion.md'])

    def test_no_completion_or_score_invented(self):
        text = '\n'.join(lp.render(self.sample()).values())
        self.assertNotIn('- [x]', text)
        self.assertNotIn('/10', text)
        self.assertIn('로컬 초안', text)

    def test_table_has_rows_and_equal_width(self):
        text = lp.table(['A', 'B'], [['one', 'two']])
        self.assertEqual(lp.lint(text), [])
        self.assertEqual(text.count('\n<tr>\n'), 2)

    def test_one_line_table_regression(self):
        self.assertTrue(lp.lint('<table header-row="true"><tr><td>x</td></tr></table>'))

    def test_escaped_table_regression(self):
        self.assertTrue(lp.lint(r'\<table header-row="true"\>\<tr\>'))

    def test_html_encoded_table_regression(self):
        self.assertTrue(lp.lint('&lt;table&gt;&lt;tr&gt;'))
        self.assertTrue(lp.lint('&#60;table&#62;'))

    def test_orphan_and_unequal_rows(self):
        self.assertTrue(lp.lint('</table>'))
        text = '<table>\n<tr>\n<td>x</td>\n</tr>\n<tr>\n<td>x</td>\n<td>y</td>\n</tr>\n</table>'
        self.assertTrue(lp.lint(text))

    def test_literal_tags_inside_cells_are_escaped(self):
        text = lp.table(['Input'], [['<page url="bad">\n**text**']])
        self.assertIn(r'\<page', text)
        self.assertNotRegex(text, r'(?<!\\)<page url=')
        self.assertEqual(lp.lint(text), [])

    def test_raw_fences_cannot_close_early(self):
        text = lp.raw_toggle('Original', '```\n<table><tr>text\n```')
        self.assertIn('````text', text)
        self.assertEqual(lp.lint(text), [])

    def test_source_file_is_byte_preserved_and_overwrite_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / 'out'
            command = [sys.executable, str(SCRIPT), 'render', str(ROOT / 'examples/lesson.synthetic.json'), '--out', str(destination)]
            result = subprocess.run(command, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((destination / 'source.json').read_bytes(), (ROOT / 'examples/lesson.synthetic.json').read_bytes())
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)

    def test_credentials_in_video_url_rejected(self):
        with self.assertRaises(ValueError):
            lp.render({'topic': 'Sample', 'video_url': 'https://name:secret@example.org/video'})


if __name__ == '__main__':
    unittest.main()
