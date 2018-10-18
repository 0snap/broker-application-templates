#!/usr/bin/python

import broker
import sys
import time

ep = broker.Endpoint()
status_subscriber = ep.make_status_subscriber(True)
ep.peer("127.0.0.1", 9999)

# blocking operation. wait until you get a status.
status = status_subscriber.get()

if type(status) != broker.Status or status.code() != broker.SC.PeerAdded:
    print("peering with remote machine failed")
    sys.exit(1)

for i in range(5):
    # send an event called "my_event"
    event = broker.bro.Event("my_event", i)
    ep.publish("demo/simple", event)

## apparently the receiver will not receive everything, if the sending process exits too early. Thus we wait here (just for the demo sake)
time.sleep(1)