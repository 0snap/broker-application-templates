#!/usr/bin/python

import time
import broker
import select
import threading
import queue

def broker_receiver(event_queue):
    ## demo receiver that is subscribed to the topic "demo/multi-threading-python"
    ep = broker.Endpoint()
    subscriber = ep.make_subscriber("demo/multi-threading-python")
    ep.listen("127.0.0.1", 9999)
    print("endpoint listening...")

    while True:
        fd_sets = select.select([subscriber.fd()], [], [])
        if not fd_sets[0]:
            print("boom. this is the end.")
        (_, data) = subscriber.get()
        event_queue.put(broker.bro.Event(data))



## we use a queue to let the broker_receiver thread communicate back to the main loop
event_queue = queue.Queue()

## spawn receiver thread such event processing and receiving are decoupled (as far as possible in python)
thread = threading.Thread(target=broker_receiver, daemon=True, args=[event_queue])
thread.start()

## we will use a bunch of workers to handle incoming messages in batches. a worker handles a batch, reports the result and then goes away.
result_queue = queue.Queue()

## work results will be handled by another thread
def handle_work_results(result_queue):
    while True:
        result = result_queue.get()
        print("have result: {}".format(result))
        result_queue.task_done()

thread = threading.Thread(target=handle_work_results, daemon=True, args=[result_queue])
thread.start()

def process_batch(batch, result_queue):
    my_sum = 0
    for event in batch:
        my_sum += 1 # event.args()[0] ## this is a number, because our sender sends numbers
    result_queue.put(my_sum)

## the main loop
PROCESS_BATCH_SIZE = 5000
while True:
    ## read a batch from the received messages.

    batch = []
    for i in range(PROCESS_BATCH_SIZE):
        batch += [event_queue.get()]
    worker = threading.Thread(target=process_batch, daemon=True, args=[batch, result_queue])
    worker.start()

