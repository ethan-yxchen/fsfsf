# -*- coding: utf-8 -*-
'''
File system related utility
'''

import os

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)


git = re.compile(br'(:$|.*/)\.git/.*')
gitignore = re.compile(br'.*\.pyc')


def listdir(path, ok):
    '''
    From one dirpath to filepaths under that dirpath

    Args:
        path: a path to a directory
        ok: a predicate (filepath) -> bool
    Returns:
        generator<filepath>
    '''
    walk, join = os.walk, os.path.join
    for (dirpath, dirnames, filenames) in walk(path):
        for filename in filenames:
            filepath = join(dirpath, filename)
            if not ok(filepath):
                continue
            yield filepath
