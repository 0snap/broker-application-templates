#include "broker/broker.hh"
#include "broker/bro.hh"
#include <sys/select.h>

using namespace broker;

// demo receiver that registers a callback to the topic "demo/select_fd"

int main() {
    endpoint ep;
    auto subscriber = ep.make_subscriber( {"demo/select_fd"} );
    ep.listen("127.0.0.1", 9999);

    fd_set fds;
    while (true) {
        FD_ZERO(&fds);
        FD_SET(subscriber.fd(), &fds);

        // this will block until we have read-readiness on the file descriptor
        auto result = select(FD_SETSIZE, &fds, nullptr, nullptr, nullptr);
        if (result == -1) {
            std::cout << "boom. this is the end." << std::endl;
            return -1;
        }

        if (FD_ISSET(subscriber.fd(), &fds)) {
            auto msg = subscriber.get(); // we could also subscriber.poll() and handle vector of messages.
            broker::topic topic(std::move(msg.first));
            bro::Event event(std::move(msg.second));
            std::cout << "received on topic: " << topic << "     event name: " << event.name() << "    content: " << event.args() << std::endl;
        }
    }

    return 0;
}
