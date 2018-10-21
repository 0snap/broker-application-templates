# App-to-App

This repo features two apps that communicate via broker, without any bro instance involved. The apps are slightly more involved and feature concurrent handling of events. For simple examples please see the other folders.


## Python multiprocessing and multithreading

Though it is possible to use multiple threads in a python application, that does still not solve the GIL problem. Thus I put another example, using the `multiprocessing` package. The whole idea of work offloading does not really fit if you just use one physical core for computions.

My experience is little with multiprocessing in python. I think it will be application dependant, wether you get a benefit from offloading to multiple processes or rather stick to the threaded solution. In case you are not doing heavy work, I think it should be fine to keep threads. The communication among them is a lot faster than inter process communication..