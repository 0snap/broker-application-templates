#include "broker/broker.hh"
#include "broker/bro.hh"
#include <unistd.h>

using namespace caf;
using namespace broker;

// demo receiver that registers a callback to the topic "demo/async_callback"

int main() {
    endpoint ep;
    ep.listen("127.0.0.1", 9999);

    ep.subscribe_nosync({ "demo/async_callback" },
        [](unit_t&) {
            // initialize, do nothing
        },
        [](unit_t&, std::pair<topic, data> msg) {
            std::cout << "async callback, not in mainloop" << std::endl;
            broker::topic topic(std::move(msg.first));
            bro::Event event(std::move(msg.second));
            std::cout << "received on topic: " << topic << "     response event name: " << event.name() << "    content: " << event.args() << std::endl;
        },
        [](unit_t&, const caf::error&) {
            // teardown, do nothing
        }
    );
    while(true) {
        std::cout << "main loop can do stuff \\o/" << std::endl;
        sleep(10);
    }
    return 0;
}