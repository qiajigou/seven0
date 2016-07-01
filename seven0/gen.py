import json
import sys
from template.flask import service_tmpl, method_tmpl


class Gen(object):
    def __init__(self):
        pass

    def load_from_path(self, path):
        with open(path) as f:
            self.load_from_json(f.read())

    def load_from_json(self, js):
        j = json.loads(js)
        self.j = j

    def load_from_dict(self, d):
        self.j = d

    def parse_imports(self, impt):
        r = impt.split('.')
        obj = r[-1]
        # ignore empty string
        path = r[1:-1]
        t = 'from {path} import {obj}\n\r'.format(
            path='.'.join(path),
            obj=obj
        )
        return t

    def parse_obj(self, impt):
        r = impt.split('.')
        return r[-1]

    def gen_tmpl(self):
        j = self.j
        service = j.get('service')

        if not service:
            return self.gen_messages()
        return self.gen_service()

    def gen_messages(self):
        # j = self.j
        return ''

    def gen_service(self):
        j = self.j
        impts = set()
        t, impls, others, mts = [], [], [], []
        service = j.get('service')
        service_name = service.keys()[0]

        t.append(service_tmpl.format(service=service_name))

        idents = service.get(service_name)
        methods = idents.get('methods')

        for method in methods:
            input_type = self.parse_obj(method.get('input_type'))
            output_type = self.parse_obj(method.get('output_type'))
            method_name = method.get('name')
            method_t = method_tmpl.format(
                method_name=method_name,
                input_type=input_type,
                output_type=output_type,
                output_obj=output_type,
                impl_name=method_name.lower(),
            )
            mts.append(method_t)
            # impts.add(method.get('input_type'))
            impts.add(method.get('output_type'))
            impls.append('from impls import {method_name}\n\r'.format(
                method_name=method.get('name').lower()))

        impts = [self.parse_imports(impt) for impt in impts]

        t.extend(impts)

        t.extend(impls)

        others.append('from seven0.utils import pb2json\n\r')

        t.extend(others)
        t.extend(mts)

        return ''.join(t)

if __name__ == '__main__':
    g = Gen()
    path = sys.argv[1:]
    path = path[0]
    g.load_from_path(path)
    print g.gen_tmpl()
