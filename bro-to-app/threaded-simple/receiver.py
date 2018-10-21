#!/usr/bin/python

import time
import broker
import select
import threading

## TAKE NOTE: without the call to select, the subscriber.get() would block the main execution python thread (GIL).
## Using select.select actually defers the waiting to the kernel. that allows our main thread to continue.

def broker_receiver():
    ## demo receiver that is subscribed to the topic "demo/threaded-simple"
    ep = broker.Endpoint()
    subscriber = ep.make_subscriber("demo/threaded-simple")
    ep.listen("127.0.0.1", 9999)
    print("endpoint listening...")

    while True:
        fd_sets = select.select([subscriber.fd()], [], [])
        if not fd_sets[0]:
            print("boom. this is the end.")
        (topic, data) = subscriber.get()
        received_event = broker.bro.Event(data)
        print("received on topic: {}    event name: {}    content: {}".format(topic, received_event.name(), received_event.args()))

## fork away a thread to receive messages via broker
thread = threading.Thread(target=broker_receiver, daemon=True)
thread.start()

while True:
    print("main loop can do stuff \\o/")
    time.sleep(1)