""":mod:`irianas_server` -- Is receiving the request sent by the client
"""
from flask import Flask
from irianas_server import metadata

app = Flask(__name__)

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright
