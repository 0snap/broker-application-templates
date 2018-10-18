# Broker Application Templates


[Bro IDS](https://www.bro.org/) ships with a communication library, called [broker](https://www.bro.org/sphinx/components/broker/broker-manual.html).

This repo provides some general purpose templates to write applications, that communicate via broker.

The project is structured as follows (see the folders):

- apps that send to a `bro` ([app-to-bro](app-to-bro))
- apps that receive from a `bro` ([bro-to-app](bro-to-app))
- apps that communicate solely via `broker`, without any `bro` instance ([standalone-apps](standalone-apps))

## Install

You need to install `broker`. Please refer to the official docs for any details. Also see the Dockerfile for an example.

The `broker` installation will bring two things:

- shared object files / libraries to link against
- python bindings

When calling `make install` with the default configuration it will put the shared object files in `/usr/local/lib`. So when you want to link against it (c++), then make sure you set your LD_LIBRARY_PATH accordingly, such that it includes `/usr/local/lib`. Python bindings will be put into `/usr/lib/python3.<X>/site-packages/broker`. Examples in this repo are meant to use `python3` only.


## Usage

Each directory comes with 2 application files

- a python application
- a c++ application

Compile the C++ files with

    g++ -std=c++11 -lbroker -lcaf_core -lcaf_io -lcaf_openssl -o <executable name> <source.cc>


Optionally, you will find one or more `.bro` scripts in there, in case the example app is communicating to a `bro` instance. To use those `.bro` scripts you need to install bro. Or you put that into a container as well.

### Bro 

In case you have a bro installed, run the scripts with (example call):

    /usr/local/bro/bin/bro ping-pong/ping_pong.bro
