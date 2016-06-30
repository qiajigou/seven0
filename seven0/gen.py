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
        t = []
        j = self.j
        impts = set()
        mts = []
        service = j.get('service')
        service_name = service.keys()[0]

        t.append(service_tmpl.format(service=service_name))

        idents = service.get(service_name)
        methods = idents.get('methods')

        for method in methods:
            input_type = self.parse_obj(method.get('input_type'))
            output_type = self.parse_obj(method.get('output_type'))
            method_t = method_tmpl.format(
                method_name=method.get('name'),
                input_type=input_type,
                output_type=output_type,
                output_obj=output_type,
            )
            mts.append(method_t)
            impts.add(method.get('input_type'))
            impts.add(method.get('output_type'))

        impts = [self.parse_imports(impt) for impt in impts]
        impts.append('from seven0.utils import pb2json\n\r')

        t.extend(impts)

        t.extend(mts)

        return ''.join(t)

if __name__ == '__main__':
    g = Gen()
    path = sys.argv[1:]
    path = path[0]
    g.load_from_path(path)
    print g.gen_tmpl()
