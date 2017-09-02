# -*- coding: utf-8 -*-
'''
Workflow related
'''

#from Queue import Queue
#import threading
import multiprocessing as mp

def producer_to_queue(producer, maxsize=10):
    '''
    Create a Queue
    Connect a generator to the Queue

    Args:
        producer: a generator
        maxsize: Queue's maxsize
    Returns:
        a tuple of <Queue, worker_process>
    '''
    q = mp.Queue(maxsize=maxsize)

    def worker():
        put = q.put
        for item in producer:
            print "pq", item
            put(item)

    process = mp.Process(target=worker)
    return q, process


def batchify(producer, batch_size):
    '''
    Collect items from producer, enumerate producer to create id,
    and then group the items into batches
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
