#include "broker/broker.hh"
#include "broker/bro.hh"
#include <unistd.h>

using namespace broker;

// demo receiver that is subscribed to the topic "demo/busy_poll"
// it runs in a loop and periodically polls everything that is available in the subscription queue (the poll itself is non blocking)

int main() {
    endpoint ep;
    auto subscriber = ep.make_subscriber( {"demo/busy_poll"} );
    ep.listen("127.0.0.1", 9999);

    // polling is not the medium of choice for true async. we need to find a way to terminate and not run forever (for this demo at least)
    for (int round = 0; round < 10; round++) {
        std::cout << "main loop busy poll..."  << std::endl;
        for (auto &msg : subscriber.poll()) {
            broker::topic topic(std::move(msg.first));
            bro::Event event(std::move(msg.second));
            std::cout << "received on topic: " << topic << "     event name: " << event.name() << "    content: " << event.args() << std::endl;
        }
        sleep(1);
    }

    return 0;
}