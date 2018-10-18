#include "broker/broker.hh"
#include "broker/bro.hh"
#include <unistd.h>

using namespace broker;

int main() {
    endpoint ep;
    auto status_subscriber = ep.make_status_subscriber(true);
    ep.peer("127.0.0.1", 9999);

    // blocking operation. wait until you get a status.
    auto stat = get_if<status>(status_subscriber.get());
    if ( !stat || stat->code() != sc::peer_added) {
        std::cerr << "peering with remote machine failed" << std::endl;
	    return 1;
    }

    for (int i = 0; i < 5; i++ ) {
        bro::Event event("my_event", {i});
        ep.publish("demo/simple", event);
    }

    // apparently the receiver will not receive everything, if the sending process exits too early. Thus we wait here (just for the demo sake)
    sleep(1);
    return 0;
}