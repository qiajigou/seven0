#!/usr/bin/env python

import sys
import json
import itertools

from google.protobuf.compiler import plugin_pb2 as plugin
from google.protobuf.descriptor_pb2 import DescriptorProto, EnumDescriptorProto


def gen(request, response):
    d = dict(messages=dict(), service=dict())
    for proto_file in request.proto_file:
        key = 'messages'
        # Parse request
        for item, package in traverse(proto_file):

            if hasattr(item, 'method'):
                key = 'service'

            d[key][item.name] = dict(
                package=proto_file.package or '&lt;root&gt;',
                filename=proto_file.name
            )

            if hasattr(item, 'field'):
                d[key][item.name].update({
                    'fields': [{'name': v.name}
                               for v in item.field]
                })

            if hasattr(item, 'value'):
                d[key][item.name].update({
                    'values': [{'name': v.name,
                                'value': v.number}
                               for v in item.value]
                })

            if hasattr(item, 'method'):
                d[key][item.name].update({
                    'methods': [{'name': v.name,
                                 'input_type': v.input_type,
                                 'output_type': v.output_type}
                                for v in item.method]
                })

            if isinstance(item, DescriptorProto):
                d[key][item.name].update({
                    'type': 'Message',
                    'properties': [{'name': f.name, 'type': int(f.type)}
                                   for f in item.field]
                })

            elif isinstance(item, EnumDescriptorProto):
                d[key][item.name].update({
                    'type': 'Enum',
                    'values': [{'name': v.name, 'value': v.number}
                               for v in item.value]
                })

        # Fill response
        f = response.file.add()
        f.name = proto_file.name + '.json'
        f.content = json.dumps(d, indent=4)


def traverse(proto_file):

    def _traverse(package, items):
        for item in items:
            yield item, package

            if isinstance(item, DescriptorProto):
                for enum in item.enum_type:
                    yield enum, package

                for nested in item.nested_type:
                    nested_package = package + item.name

                    for nested_item in _traverse(nested, nested_package):
                        yield nested_item, nested_package

    return itertools.chain(
        _traverse(proto_file.package, proto_file.enum_type),
        _traverse(proto_file.package, proto_file.message_type),
        _traverse(proto_file.package, proto_file.service),
    )


def parse():
    data = sys.stdin.read()
    request = plugin.CodeGeneratorRequest()
    request.ParseFromString(data)
    response = plugin.CodeGeneratorResponse()
    gen(request, response)
    output = response.SerializeToString()
    sys.stdout.write(output)


if __name__ == '__main__':
    parse()
