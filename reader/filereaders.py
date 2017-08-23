'''
path => generator<str>
'''

import os
from mmap import mmap, ACCESS_READ
import threading

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)


def ListDirRecursive(path, ok):
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


def batchify(producer, batch_size):
    '''
    Collect items from producer, enumerate producer to create id, generate
    batches
    '''
    batch = []
    append = batch.append
    for item in enumerate(producer):
        append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
            append = batch.append
    if batch:
        yield batch


def produce_to_queue(producer, maxsize=10):
    q = Queue(maxsize=maxsize)

    def worker():
        put = q.put
        for item in producer:
            put(item)
        put(None)

    t = threading.Thread(target=worker)
    return q, t


def open_rdonly(filepath):
    return os.open(filepath, os.O_RDONLY)


def mmap_reader(filepath):
    meta = {'filepath': filepath}
    return mmap(open_rdonly(filepath), 0, access=ACCESS_READ), meta
