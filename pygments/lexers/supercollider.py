"""
    pygments.lexers.supercollider
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for SuperCollider

    :copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, include, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation

__all__ = ['SuperColliderLexer']


class SuperColliderLexer(RegexLexer):
    """
    For SuperCollider source code.
    """

    name = 'SuperCollider'
    url = 'http://supercollider.github.io/'
    aliases = ['supercollider', 'sc']
    filenames = ['*.sc', '*.scd']
    mimetypes = ['application/supercollider', 'text/supercollider']
    version_added = '2.1'

    flags = re.DOTALL | re.MULTILINE
    tokens = {
        # Multiline comments can nest.
        'multiline_comment': [
            (r'[^*/]+', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline)
        ],
        # Double-quote strings can be multiline.
        'string': [
            (r'\\[nt]', String.Escape),
            (r'.*?"', String, '#pop')
        ],
        'root': [
            (r'(\s+|\t+|\n)+', Text.Whitespace),
            (r'//.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline_comment'),
            (r'"', String, 'string'),
            # Single-quote symbol.
            (r"'.*?'", String.Symbol),
            # Alphanumeric backslash symbol.
            (r'\\[a-zA-Z0-9]+', String.Symbol),
            # Empty symbol.
            (r'\\', String.Symbol),
            (r'\$.', String.Char),
            (r'([()\[\]\{\}.;:#=,`\^|]|<-)', Punctuation),
            (r'[!@%&*\-+=<>?/]+', Operator),
            # Floats must have a period, exponent suffix, or both. If period is
            # present there must be digits to either side.
            (r'\d+\.\d+([eE]-?\d+)?', Number.Float),
            (r'\d+[eE]-?\d+', Number.Float),
            (r'\d+', Number.Integer),
            # TODO: radix, 1s/1b syntax for numeric literals
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (words([
                "var", "const", "class", "arg", "classvar", "this",
                "thisThread", "thisMethod", "thisFunction", "thisFunctionDef",
                "thisProcess", "true", "false", "inf", "nil", "context"
            ], suffix=r'\b'), Keyword),
            # Matches both key binary operators and argument names.
            (r'[a-z][a-zA-Z0-9_]*:', Name),
            (r'[a-z][a-zA-Z0-9_]*', Name),
            (r'[A-Z][a-zA-Z0-9_]*', Name.Class),
        ]
    }

    def analyse_text(text):
        """We're searching for a common function and a unique keyword here."""
        if 'SinOsc' in text or 'thisFunctionDef' in text:
            return 0.1
