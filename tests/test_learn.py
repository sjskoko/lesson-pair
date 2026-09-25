import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

path = Path(__file__).resolve().parents[1] / 'skills/lesson-pair/scripts/learn.py'
spec = importlib.util.spec_from_file_location('learn', path)
learn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(learn)

class Handler(BaseHTTPRequestHandler):
    requests = []
    status = 200
    content = 'AI feedback with one practice question.'
    def log_message(self, *args): pass
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.requests.append((self.path, self.headers.get('Authorization'), body))
        self.send_response(self.status)
        if self.status == 302:
            self.send_header('Location', '/stolen')
        self.end_headers()
        if self.status == 200:
            self.wfile.write(json.dumps({'choices': [{'message': {'content': self.content}}]}).encode())
        else:
            self.wfile.write(b'private server body must never appear in errors')

class TutorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()
    def setUp(self):
        Handler.requests = []; Handler.status = 200; Handler.content = 'AI feedback with one practice question.'
        self.provider = learn.Provider(f'http://127.0.0.1:{self.server.server_port}/v1', 'test-model', 'TEST-SECRET')
        self.session = learn.new_session('Trees provide shade. Roots need room.', 'synthetic fixture', 'Korean')
    def test_vtt_and_srt(self):
        self.assertEqual(learn.normalize_transcript('WEBVTT\n\n00:00.000 --> 00:02.000\n<c>Trees provide shade.</c>\n\n00:02.000 --> 00:03.000\nTrees provide shade.\nRoots need room.'), 'Trees provide shade.\nRoots need room.')
        self.assertEqual(learn.normalize_transcript('1\n00:00:01,000 --> 00:00:02,000\nTrees &amp; roots.'), 'Trees & roots.')
    def test_empty_and_long_source_rejected(self):
        for raw in ('WEBVTT\n\n', 'x' * 24001):
            with self.assertRaises(ValueError): learn.new_session(raw, 'fixture')
    def test_originals_and_provider_contract(self):
        first = 'Trees makes shade.  Roots need place.'
        learn.record_answer(self.session, first)
        learn.finish_pending(self.session, self.provider)
        self.assertEqual(self.session['attempts'][0]['text'], first)
        self.assertEqual(self.session['stage'], 'practice')
        route, auth, body = Handler.requests[-1]
        self.assertEqual(route, '/v1/chat/completions')
        self.assertEqual(auth, 'Bearer TEST-SECRET')
        self.assertEqual(body['model'], 'test-model')
        self.assertIn(first, body['messages'][1]['content'])
        self.assertNotIn('TEST-SECRET', json.dumps(self.session))
    def test_failure_resume_never_duplicates_or_loses_attempt(self):
        learn.record_answer(self.session, 'Trees makes shade.')
        Handler.status = 401
        with self.assertRaisesRegex(ValueError, 'HTTP 401') as ctx:
            learn.finish_pending(self.session, self.provider)
        self.assertNotIn('private server', str(ctx.exception))
        self.assertEqual(self.session['pending'], 'baseline')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 's.json'; learn.save_session(p, self.session)
            resumed = learn.load_session(p)
            Handler.status = 200; learn.finish_pending(resumed, self.provider)
        self.assertEqual(len(resumed['attempts']), 1)
        self.assertEqual(resumed['stage'], 'practice')
    def test_no_redirect_key_leak(self):
        Handler.status = 302
        learn.record_answer(self.session, 'Trees make shade.')
        with self.assertRaisesRegex(ValueError, 'HTTP 302'):
            learn.finish_pending(self.session, self.provider)
        self.assertEqual(len(Handler.requests), 1)
    def test_endpoint_validation(self):
        for url in ('http://example.com/v1', 'https://user:key@example.com/v1', 'https://example.com/v1?key=secret', 'file:///tmp/provider', 'https://example.com/#fragment'):
            with self.assertRaises(ValueError): learn.Provider(url, 'model')
    def test_malformed_provider_response_preserves_pending(self):
        Handler.content = None
        learn.record_answer(self.session, 'Trees make shade.')
        with self.assertRaises(ValueError): learn.finish_pending(self.session, self.provider)
        self.assertEqual(self.session['pending'], 'baseline')
        self.assertFalse(self.session['feedback'])
    def test_complete_session_with_hint_and_evidence_export(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 's.json'; learn.save_session(p, self.session)
            inputs = iter(['Trees makes shade.', '/hint', 'Roots need room.', 'Trees provide shade. Roots need space.', 'yes'])
            learn.run_session(p, self.provider, lambda _: next(inputs), lambda _: None)
            saved = learn.load_session(p)
        self.assertEqual(saved['stage'], 'done')
        self.assertEqual(saved['assistance'], ['hint'])
        self.assertEqual(saved['retry_assistance'], 'assisted (self-reported)')
        self.assertEqual(len(saved['attempts']), 3)
        exported = learn.export_markdown(saved)
        self.assertIn('Learner baseline — original', exported)
        self.assertIn('AI feedback — retry', exported)
        self.assertNotIn('TEST-SECRET', exported)
        self.assertIn('- [ ]', exported)
    def test_retry_survives_eof_before_assistance_answer(self):
        self.session['stage'] = 'retry'
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 's.json'; learn.save_session(p, self.session)
            calls = iter(['Roots need room.'])
            def answer(_):
                try: return next(calls)
                except StopIteration: raise EOFError
            learn.run_session(p, self.provider, answer, lambda _: None)
            saved = learn.load_session(p)
        self.assertEqual(saved['attempts'][-1]['text'], 'Roots need room.')
        self.assertEqual(saved['pending'], 'retry')
        self.assertEqual(saved['retry_assistance'], 'unknown')
    def test_no_invented_retry(self):
        learn.record_answer(self.session, 'First attempt.')
        learn.finish_pending(self.session, self.provider)
        self.assertNotIn('retry', [a['stage'] for a in self.session['attempts']])
        self.assertNotIn('Learner retry', learn.export_markdown(self.session))
    def test_pending_task_blocks_new_answer(self):
        learn.record_answer(self.session, 'Original.')
        with self.assertRaises(ValueError): learn.record_answer(self.session, 'Replacement.')
        self.assertEqual(len(self.session['attempts']), 1)

if __name__ == '__main__': unittest.main()
