module Demo;

export {
    redef enum Log::ID += {
        LOG
    };
    redef LogAscii::empty_field = "";

    type Info: record {
        msg: string &log;
    };

    global log: function(msg: string);
}

event bro_init() &priority=5 {
    Log::create_stream(Demo::LOG, [$columns=Info, $path="demo"]);
}

function log(msg: string) {
    Log::write(LOG, [$msg=msg]);
}
