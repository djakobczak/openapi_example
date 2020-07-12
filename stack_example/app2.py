from flask import Flask, jsonify, abort, make_response, request
from flask.views import MethodView
from flasgger import Swagger, swag_from
import os
from settings import PATH_TO_OPENAPI
from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator
from openapi_core import create_spec
from os import path
from openapi_spec_validator.schemas import read_yaml_file
from openapi_core.contrib.flask.views import FlaskOpenAPIView


# looks like validation works properly
# !TODO check $ref: looks good
# - responses are validated

# bug in openapi core:
# if method returns just a string (not an object) then it raises Exception "AttributeError: 'str' object has no attribute 'data'"

# Openapi core validation process:
# 1. get request
# 2. validate against openapi parameters and request body
# 3. check errors 
# 4. get response
# 5. validate against openapi response (code+content)


# !TODO check plantext requestBody and other types (json works)

FILE = 'openapi3.yml'
FILE2 = 'openapi.yml'

def spec_from_file(spec_file):
    directory = path.abspath(path.dirname(__file__))
    path_full = path.join(directory, spec_file)
    return read_yaml_file(path_full)


def spec_dict():
    return spec_from_file(FILE)


# print(spec_dict())
spec = create_spec(spec_dict())
openapi = FlaskOpenAPIViewDecorator.from_spec(spec)

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Test API',
}
app.config['SWAGGER']['openapi'] = '3.0.0'
swagger = Swagger(app=app, template_file=FILE)


class UserAPI(MethodView):
    decorators = [openapi]
    def get(self):
        return jsonify({'id': int(request.args.get('userId')), 'name': 'NORMAL'})

class HostnameChange(MethodView):
    decorators = [openapi]
    def post(self):
        print('Post incomming')
        print(request.json)
        return jsonify({'response': 'ok'})      # openapi core validates response (it must match with openapi yml) 


@app.route('/home')
@openapi
def home():
    return jsonify({'home': 'ok'})

@app.route('/info')
@openapi
def info():
    return jsonify({'info': request.args.get('infoName')})

app.add_url_rule('/users/', view_func=UserAPI.as_view('users'), methods=['GET'])
app.add_url_rule('/hostname/', view_func=HostnameChange.as_view('hostname'), methods=['POST'])

# OpenAPI file has to have the same path e.g. '/users/ not /users


app.run(debug=True)