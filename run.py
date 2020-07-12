import os

from flask import Flask, request, jsonify, Response
from flasgger import Swagger, swag_from


app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Flasgger Parsed Method/Function View Example'
}

swag = Swagger(app)

@app.route('/api/user/')
@swag_from("docs/user.yml", validation=True)
def user():
    """Flasgger will try to load './user.yml' as swagger doc
    """
    return jsonify({'age': request.args.get('age')})

@app.route('/api/pet/')
def pet():
    """Flasgger will try to load './pet.yml' as swagger doc
    """
    return jsonify({'name': request.args.get('name'), 'owner': request.args.get('owner')})


if __name__ == '__main__':
    app.run(debug=True)
