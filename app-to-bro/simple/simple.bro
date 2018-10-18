redef exit_only_after_terminate = T;

## event handler. is invoked, when something is received (on any topic) that claims the name "my_event"
event my_event(i: int) {
    print "my_event", i;
}

## event handler. is invoked, whenever something connects via broker
event Broker::peer_added(endpoint: Broker::EndpointInfo, msg: string) {
    print "peer added", endpoint$network$address;
}

event bro_init() {
	Broker::subscribe("demo/simple");
	Broker::listen("0.0.0.0", 9999/tcp);
	print "bro init";
}
