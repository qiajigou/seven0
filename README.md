# seven0

This project is a tiny gRPC utils project. gRPC is using protobuf, everytime change the protobuf, we have to regencode.

And if we want more options in protobuf, such as options, we will die.

Fake code below:

```protobuf
syntax = "proto3";

import "google/protobuf/descriptor.proto";

extend google.protobuf.MethodOptions {
    MO mo = 50006;
}

message MO {
    string method = 1;
    string url    = 2;
}

message HelloRequest {
    string say    = 1;
}

message HelloResponse {
    string reply  = 1;
}

service SimpleService {

    // this should be http://yourdomain/service/r2d2/hello
    // and the method should be GET
    rpc Hello(HelloRequest) returns (HelloResponse) {
        option (mo).method = "GET";
        option (mo).url    = "/service/r2d2/hello"
    };

}
```

The default protobuf plugin which supported by gRPC and protobuf does not support this feature.

Most of the time we don't need this tool in our projects. BUT. If we have a lots of gRPC server, or just want a gRPC Python client, this WILL help.

# Client

Everytime we write a protobuf file, and we want a gRPC python client.

we could use this tool to generate a gRPC python client.

# Server

And of course, we could generate Server by using this tool.

And we could generate Server also support HTTP protocol with customized options.

# gRPC gateway

We could use [c3po-grpc-gateway](https://github.com/qiajigou/c3po-grpc-gateway) to translate gRPC to HTTP protocol, so we need a dynamic client. This will help.

# gRPC server

After generate the server side code, we need a gunicorn like gRPC server handler, [grma](https://github.com/qiajigou/grma) should help.

This tool make sure we don't need to write a server and client everytime.

# How to use

Goto example and run:

```
./gencode.sh
```

You should find out the rpc client and pb files.

# TODO

This is in early develop.
