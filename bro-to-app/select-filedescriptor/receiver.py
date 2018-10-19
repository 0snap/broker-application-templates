#!/usr/bin/python

import broker
import select

## demo receiver that is subscribed to the topic "demo/select_fd"

ep = broker.Endpoint()
subscriber = ep.make_subscriber("demo/select_fd")
ep.listen("127.0.0.1", 9999)

while(True):

    ## this will block until we have read-readiness on the file descriptor
    # print("wait ...")
    fd_sets = select.select([subscriber.fd()], [], [])
    # print ("go on...")
    if not fd_sets[0]:
        print("boom. this is the end.")

    (topic, data) = subscriber.get() #// we could also subscriber.poll() and handle array of messages
    received_event = broker.bro.Event(data)

    print("received on topic: {}    event name: {}    content: {}".format(topic, received_event.name(), received_event.args()))


## in fact, with a blocking select this is pretty similar to the "simple" example. The call to `subscriber.get()` blocks as well. To handle this nicely, we have to wrap it into a thread.