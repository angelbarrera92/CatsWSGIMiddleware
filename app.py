from flask import Flask
from CatsWSGIMiddleware import CatsMiddleware

app = Flask(__name__)


@app.route('/')
def main():
    return 'hola'

wrapped_app = CatsMiddleware(app)
