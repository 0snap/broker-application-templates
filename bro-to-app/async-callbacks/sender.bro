redef exit_only_after_terminate = T;

## global definition of an event with name "greet"
global greet: event(msg: string, i: int);

## event handler. is invoked, whenever something connects via broker
## this works in either direction, so it would get fired when we receive a connection on bro side or when we establish a connection from bro to our receiving app.
event Broker::peer_added(endpoint: Broker::EndpointInfo, msg: string) {
	print "peering successful", endpoint;
	print "will send some greetings";

	local i = 0;
	while (i < 10) {

		## creating this event will auto publish it (see the bro_init event)
		event greet("hi there", ++i);
	}

	## schedule the greet event to be invoked in 2sec in the future (for the demo's sake to see the polling of the receiver)
	schedule 2sec { greet("bye", 1000) };

	# terminate(); -> we cannot use this here. otherwise the scheduled event would fire immediately (short circuit schedule)
}

event greet(msg: string, i: int) {
	## this is just to make the bro script terminate
	## it is needed, because i wanted to add a scheduled event
	if (i == 1000) {
		terminate();
	}
}

event bro_init() {
	Broker::peer("127.0.0.1", 9999/tcp, 2sec);

	## whenever the event "greet" is called, it will be published automatically on the topic "demo/async_callback"
    Broker::auto_publish("demo/async_callback", greet);
	print "bro init";
}
