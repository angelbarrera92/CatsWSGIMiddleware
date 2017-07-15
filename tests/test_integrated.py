import signal
import subprocess
import time
from contextlib import contextmanager

from CatsWSGIMiddleware import CatsMiddleware
import requests


def app_custom_error(environ, start_response):
    start_response(
        "418 I'm a teapot",
        [('Content-Type', 'text/plain')]
    )
    return [b"I'm a teapot"]


def app_without_cats(environ, start_response):
    start_response(
        '200 OK',
        [('Content-Type', 'text/html')]
    )
    return [b'<h1>Fine</h1>']

wrapped_app_without_cats = CatsMiddleware(app_without_cats)
wrapped_app_custom_error = CatsMiddleware(app_custom_error)
wrapped_app_hatting_cats = CatsMiddleware(app_without_cats, i_hate_cats=True)


@contextmanager
def run_gunicorn(app_name):
    command = ['gunicorn', __name__ + ':' + app_name]
    process = subprocess.Popen(command)
    time.sleep(1)  # Let gunicorn start
    try:
        yield
    finally:
        process.send_signal(signal.SIGINT)
        process.wait()


def test_wrapped_app_without_cats():
    with run_gunicorn('wrapped_app_without_cats'):
        resp = requests.get('http://localhost:8000')
        assert resp.status_code == 200
        assert resp.text == '<h1>Fine</h1>'


def test_wrapped_app_with_cats():
    with run_gunicorn('wrapped_app_without_cats'):
        headers = {
            'Cats': 'Ouuu Yeah!'
        }
        resp = requests.get('http://localhost:8000', headers=headers)
        assert resp.status_code == 200
        assert resp.headers.get('Cats') == '=^..^='


def test_wrapped_app_with_hatting_cats():
    with run_gunicorn('wrapped_app_hatting_cats'):
        resp = requests.get('http://localhost:8000')
        assert resp.status_code == 200
        assert resp.headers.get('Cats') == '=^..^='


def test_wrapped_app_custom_error():
    with run_gunicorn('wrapped_app_custom_error'):
        resp = requests.get('http://localhost:8000')
        assert resp.status_code == 418
        assert resp.headers.get('Cats') == '=^..^='
