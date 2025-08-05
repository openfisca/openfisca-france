#! /usr/bin/env python

import os
import re
import tokenize


DOUBLE_QUOTE_DOCSTRING_RE = re.compile(
    r'''^(?P<prefix>[furbFURB]*)"""(?P<content>.*?)"""$''',
    re.DOTALL)
DOUBLE_QUOTE_STRING_RE = re.compile(
    r'''^(?P<prefix>[furbFURB]*)"(?P<content>[^']*)"$''')
# SINGLE_QUOTE_DOCSTRING_RE = re.compile(
#     r"""^(?P<prefix>[furbFURB]*)'''(?P<content>.*?)'''$""",
#     re.DOTALL)
# SINGLE_QUOTE_STRING_RE = re.compile(
#     r"""^(?P<prefix>[furbFURB]*)'(?P<content>[^"]*)'$""")


def iterate_tokens(file_path):
    with open(file_path, encoding='utf-8') as python_file:
        for token in tokenize.generate_tokens(python_file.readline):
            if token.type == tokenize.STRING:
                token = token._replace(string=DOUBLE_QUOTE_DOCSTRING_RE.sub(
                    r"\g<prefix>'''\g<content>'''",  # noqa: W605
                    token.string))
                token = token._replace(string=DOUBLE_QUOTE_STRING_RE.sub(
                    r"\g<prefix>'\g<content>'",  # noqa: W605
                    token.string))
            yield token


project_dir = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
for path, dirs, files in os.walk(project_dir):
    for dir in dirs:
        if dir.startswith('.') and dir != '.github':
            dirs.remove(dir)
    for file in files:
        if file.startswith('.') or not file.endswith('.py'):
            continue
        file_path = os.path.join(path, file)
        normalized_source_code = tokenize.untokenize(iterate_tokens(file_path))
        with open(file_path, 'w', encoding='utf-8') as python_file:
            python_file.write(normalized_source_code)
