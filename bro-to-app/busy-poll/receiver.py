#!/usr/bin/python

import broker
import sys
import time

## demo receiver that is subscribed to the topic "demo/busy_poll"
## it runs in a loop and periodically polls everything that is available in the subscription queue (the poll itself is non blocking)

ep = broker.Endpoint()
subscriber = ep.make_subscriber("demo/busy_poll")
ep.listen("127.0.0.1", 9999)

## polling is not the medium of choice for true async. we need to find a way to terminate and not run forever (for this demo at least)

for i in range(10):
    print("poll...")
    for msg in subscriber.poll():
        (topic, data) = msg
        received_event = broker.bro.Event(data)
        print("received on topic: {}    event name: {}    content: {}".format(topic, received_event.name(), received_event.args()))
    
    time.sleep(1)