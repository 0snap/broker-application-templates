#include "broker/broker.hh"
#include "broker/bro.hh"

using namespace broker;

// this thing has two directions:
// it sends and receives. thus it needs to be a subscriber
int main() {
    endpoint ep;
    auto subscription = ep.make_subscriber( {"demo/ping_pong"} );
    auto status_subscriber = ep.make_status_subscriber(true);
    ep.peer("127.0.0.1", 9999);

    // blocking operation. wait until you get a status.
    auto stat = get_if<status>(status_subscriber.get());
    if ( !stat || stat->code() != sc::peer_added) {
        std::cerr << "peering with remote machine failed" << std::endl;
	    return 1;
    }

    for (int i = 0; i < 5; i++ ) {
        // the bro on the other side needs to have an event handler called "ping".
        bro::Event event("ping", {i});
        ep.publish("demo/ping_pong", event);

        // blocking operation. wait until at least 1 message is available and take it.
        auto msg = subscription.get();
        broker::topic topic(std::move(msg.first));
        bro::Event response(std::move(msg.second));
        std::cout << "received on topic: " << topic << "     response event name: " << response.name() << "    content: " << response.args() << std::endl;
    }

    return 0;
}