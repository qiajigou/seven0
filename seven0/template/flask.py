service_tmpl = '''# Service name {service}

from flask import Flask
from flask import jsonify

app = Flask(__name__)

'''

method_tmpl = '''

@app.route("/{method_name}")
def {method_name}():
    # input type: {input_type}
    # output type: {output_type}
    d = {method_name}Impl()
    r = {output_type}(**d)
    return jsonify(pb2json(r))
'''
