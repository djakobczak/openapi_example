from flask import Flask, jsonify, abort, make_response, request
from flask.views import MethodView
from flasgger import Swagger, swag_from
import os
from settings import PATH_TO_OPENAPI

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Test API',
}
app.config['SWAGGER']['openapi'] = '3.0.0'
swagger = Swagger(app=app, template_file=PATH_TO_OPENAPI, parse=True)


class GetUser(MethodView):
    def get(self):
        return jsonify({'id': request.args.get('userId'), 'type': 'NORMAL'})

class GetGroup(MethodView):
    def get(self):
        return jsonify({'name': request.args.get('groupName'), 'type': 'NORMAL'})


app.add_url_rule(
    '/users/', view_func=GetUser.as_view(name='users'),
    methods=['GET'])

app.add_url_rule(
    '/groups/', view_func=GetGroup.as_view(name='groups'),
    methods=['GET'])

app.run(debug=True)