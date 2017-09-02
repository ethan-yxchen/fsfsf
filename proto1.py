#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
from multiprocessing import Process
import os

try:
    import re2 as re
except ImportError:
    import re
else:
    re.set_fallback_notification(re.FALLBACK_WARNING)

from files import git, gitignore, listdir
from flows import producer_to_queue, batchify

from tokenization import test

def ignore(filepath):
    return not git.match(filepath) and not gitignore.match(filepath)

ascii_space = re.compile(br'[\s]')
ascii_alnum = re.compile(br'[\w]+')
f = ascii_alnum.findall
g = ascii_space.split

def read(doc_id, path):
    document = open(path, 'rb').read()
    meta = {'doc_id': doc_id, 'path': path}
    print meta
    try:
        meta['tokens'] = test(document, len(document))
    except UnicodeDecodeError:
        pass


def run_single_process(batch_producer, do_job):
    '''
    Why batch? Batches can make multiprocessing more efficient; and we want
    single and multiprocessing versions has the same interface
    '''
    for batch in batch_producer:
        for item in batch:
            do_job(*item)


def run_multi_process(batch_producer, do_job, num_workers):
    queue, producer_process = producer_to_queue(batch_producer, num_workers + 2)
    producer_process.start()

    def worker():
        for batch in iter(queue.get, None):
            for item in batch:
                do_job(*item)

    workers = [Process(target=worker) for i in range(num_workers)]
    for i in workers:
        i.start()

    producer_process.join()
    for i in workers:
        queue.put(None)
    for i in workers:
        i.join()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('path')
    arg_parser.add_argument('nproc', type=int)
    arg_parser.add_argument('bsize', type=int)
    arg_parser.add_argument('--single', action='store_true')
    args = arg_parser.parse_args()

    dirs = listdir(args.path, ignore)
    dirbatch = batchify(dirs, args.bsize)

    if args.single:
        run_single_process(dirbatch, read)
    else:
        run_multi_process(dirbatch, read, args.nproc)
    # queue, proc_enum_dir = producer_to_queue(dirbatch, args.nproc + 3)
    # proc_enum_dir.start()
    #
    # def worker():
    #     for batch in iter(queue.get, None):
    #         for item in batch:
    #             read(*item)
    #
    # t = [Process(target=worker) for i in range(args.nproc)]
    # for i in t:
    #     i.start()
    # proc_enum_dir.join()
    # for i in t:
    #     queue.put(None)
    # queue.put(None)
    # for i in t:
    #     i.join()
    #worker()


if __name__ == "__main__":
    main()
