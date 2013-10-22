#!/usr/bin/env python
""":mod:`irianas_server.main` -- Program entry point
"""
import sys
sys.path[0:0] = [""]
from irianas_server.core import build_app
from irianas_server import app


def main():

    app.secret_key = 'as90kSDKO#1@|4245losadim'
    build_app(app)
    app.run(debug=True)

if __name__ == '__main__':
    main()
