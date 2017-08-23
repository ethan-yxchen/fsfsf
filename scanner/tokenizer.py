'''
str => list<str>
'''
from collections import namedtuple

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)

unicode_alnum = re.compile(r'[\w]+', flags=re.UNICODE)
unicode_space = re.compile(r'[\s]', flags=re.UNICODE)

ascii_alnum = re.compile(br'[\w]+')
ascii_space = re.compile(br'[\s]')

TokensPos = namedtuple('TokensPos', ('tokens', 'pos'))


def tokens_pos(regex):
    def func(s):
        tokens, pos = [], []
        append_tokens, append_pos = tokens.append, pos.append
        for match in regex.finditer(s):
            append_tokens(match.group(0))
            append_pos(match.pos)
        return TokensPos(tokens, pos)
    return func
