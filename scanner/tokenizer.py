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

def tokens_pos(regex):
    TokensPos = namedtuple('TokensPos', ('tokens', 'pos'))
    def func(s):
        tokens, pos = [], []
        for match in regex.finditer(s):
            tokens.append(match.group(0))
            pos.append(match.pos)
        return TokensPos(tokens, pos)
    return func
