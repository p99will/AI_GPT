from flask import Flask, request, jsonify
import os
import openai
import re
import webbrowser
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import requests