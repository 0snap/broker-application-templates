@load ./log

## same example code as in ping_pong
## additionally to printing, it logs stuff to a file

redef exit_only_after_terminate = T;

global pong: event(n: int);

## event handler. is invoked, when something is received (on any topic) that claims the name "ping"
event ping(i: int) {
    ## call the event pong
    ## this event will be published automatically. See bro_init()
    event pong(i);
    print "received ping", i;
    Demo::log(fmt("received ping %d", i));
}

## event handler. is invoked, whenever something connects via broker
event Broker::peer_added(endpoint: Broker::EndpointInfo, msg: string) {
    print "peer added", endpoint$network$address;
    Demo::log("peer added " + endpoint$network$address);
}

event bro_init() {
	Broker::subscribe("demo/ping_pong");
	Broker::listen("0.0.0.0", 9999/tcp);

    ## whenever the event "pong" is called, it will be published automatically on the topic "demo/ping_pong"
    Broker::auto_publish("demo/ping_pong", pong);
	print "bro init";

    Demo::log("bro init");
}