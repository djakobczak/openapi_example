from flask import Flask, jsonify, abort, make_response, request
from flasgger import Swagger, swag_from
import os

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'My API',
}
app.config['SWAGGER']['openapi'] = '3.0.0'

conf_path = os.path.abspath(__file__)
conf_path = os.path.dirname(conf_path)
conf_path = os.path.join(conf_path, 'openapi', 'api.yml')
swagger = Swagger(app=app, template_file=conf_path)

@app.route('/pets', methods=['GET'])
@swag_from('./openapi/api.yml', validation=True)
def pets():
    """
    Test function
    Some test function for debugging Swagger.
    """
    return jsonify({"var1": request.args.get('limit'), "var2":"sdfsdf"})

app.run(debug=True)