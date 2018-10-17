# Broker Application Templates


[Bro IDS](https://www.bro.org/) ships with a communication library, called [broker](https://www.bro.org/sphinx/components/broker/broker-manual.html).

This repo provides some general purpose templates to write applications, that communicate via broker.

## Install

You need to install `broker`. Please refer to the official docs for any details. Also see the Dockerfile for an example.

The `broker` installation will bring two things:

- shared object files / libraries to link against
- python bindings

When calling `make install` with the default configuration it will put the shared object files in `/usr/local/lib`. So when you want to link against it (c++), then make sure you set your LD_LIBRARY_PATH accordingly, such that it includes `/usr/local/lib`. Python bindings will be put into `/usr/lib/python3.<X>/site-packages/broker`. Examples in this repo are meant to use `python3` only.


## Usage

Each directory comes with at least 3 files:

- a `.bro` file, that instructs bro how to handle incoming events
- a python application
- a c++ application

When you want to have a bro IDS to handle the events, you need to install bro. Or you put that into a container as well.

Compile the C++ files with

    g++ -std=c++11 -lbroker -lcaf_core -lcaf_io -lcaf_openssl -o <executable name> <source.cc>

### Bro 

In case you have a bro installed, run the scripts with (example):

    /usr/local/bro/bin/bro ping-pong/ping_pong.bro