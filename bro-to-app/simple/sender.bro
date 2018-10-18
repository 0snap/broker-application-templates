redef exit_only_after_terminate = T;

## global definition of an event with name "my_event"
global my_event: event(msg: string);

## event handler. is invoked, whenever something connects via broker
## this works in either direction, so it would get fired when we receive a connection on bro side or when we establish a connection from bro to our receiving app.
event Broker::peer_added(endpoint: Broker::EndpointInfo, msg: string) {
	print "peering successful", endpoint;
	print "will send two events...";
	## create explicitly
	local event_0 = Broker::make_event(my_event, "hi");
	Broker::publish("demo/simple", event_0);

	## inline
	Broker::publish("demo/simple", my_event, "there");

	print "sent two events";
	terminate();
}

event bro_init() {
	## the third param makes broker retry to peer every 2 seconds
	Broker::peer("127.0.0.1", 9999/tcp, 2sec);
	print "bro init";
}
