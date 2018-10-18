#include "broker/broker.hh"
#include "broker/bro.hh"

using namespace broker;

// demo receiver that is subscribed to the topic "demo/simple"
int main() {
    endpoint ep;
    auto subscriber = ep.make_subscriber( {"demo/simple"} );
    ep.listen("127.0.0.1", 9999);

    // block until at least two messages are available (for non blocking receiver see "non-blocking" example app)
    auto messages = subscriber.get(2);

    for (auto &msg : messages) {
        broker::topic topic(std::move(msg.first));
        bro::Event response(std::move(msg.second));
        std::cout << "received on topic: " << topic << "     response event name: " << response.name() << "    content: " << response.args() << std::endl;
    }

    return 0;
}