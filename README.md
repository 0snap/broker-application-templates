# Broker Application Templates


[Bro IDS](https://www.bro.org/) ships with a communication library, called [broker](https://www.bro.org/sphinx/components/broker/broker-manual.html).

This repo provides some general purpose templates to write applications, that communicate via broker.

## Install

You need to install `broker`. Please refer to the official docs for any details. Also see the Dockerfile for an example.

The `broker` installation will bring two things:

- shared object files / libraries to link against
- python bindings

When calling `make install` with the default configuration it will put the shared object files in `/usr/local/lib`. So when you want to link against it (c++), then make sure you set your LD_LIBRARY_PATH accordingly, such that it includes `/usr/local/lib`. Python bindings will be put into `/usr/lib/python3.<X>/site-packages/broker`. Examples in this repo are meant to use `python3` only.




