#!/usr/bin/python

import time
import broker
import select
import multiprocessing

def broker_receiver(event_queue):
    ## demo receiver that is subscribed to the topic "demo/multi-processing-python"
    ep = broker.Endpoint()
    subscriber = ep.make_subscriber("demo/multi-processing-python")
    ep.listen("127.0.0.1", 9999)
    print("endpoint listening...")

    while True:
        fd_sets = select.select([subscriber.fd()], [], [])
        if not fd_sets[0]:
            print("boom. this is the end.")
        (_, data) = subscriber.get()
        event = broker.bro.Event(data)
        event_queue.put([event.name(), event.args()])



## we use a queue to let the broker_receiver process communicate back to the main loop
event_queue = multiprocessing.Queue()

## spawn receiver process such event processing and receiving are decoupled (as far as possible in python)
process = multiprocessing.Process(target=broker_receiver, args=[event_queue])
process.start()

## we will use a bunch of workers to handle incoming messages in batches. a worker handles a batch, reports the result and then goes away.
result_queue = multiprocessing.Queue()

## work results will be handled by another process
def handle_work_results(result_queue):
    while True:
        result = result_queue.get()
        print("have result: {}".format(result))

process = multiprocessing.Process(target=handle_work_results, args=[result_queue])
process.start()

def process_batch(batch, result_queue):
    my_sum = 0
    for event in batch:
        my_sum += event[1][0]
    result_queue.put(my_sum)

## the main loop
PROCESS_BATCH_SIZE = 5000
worker_num = 0
while True:
    ## read a batch from the received messages.
    batch = []
    for i in range(PROCESS_BATCH_SIZE):
        batch += [event_queue.get()]
    print("started worker_num", worker_num)
    worker_num += 1
    worker = multiprocessing.Process(target=process_batch, args=[batch, result_queue])
    worker.start()

