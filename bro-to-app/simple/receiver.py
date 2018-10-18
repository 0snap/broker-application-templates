#!/usr/bin/python

import broker
import sys

## demo receiver that is subscribed to the topic "demo/simple"

ep = broker.Endpoint()
subscriber = ep.make_subscriber("demo/simple")
ep.listen("127.0.0.1", 9999)

## block until at least two messages are available (for non blocking receiver see "non-blocking" example app)
messages = subscriber.get(2)
for msg in messages:
    (topic, data) = msg
    received_event = broker.bro.Event(data)
    print("received on topic: {}    event name: {}    content: {}".format(topic, received_event.name(), received_event.args()))