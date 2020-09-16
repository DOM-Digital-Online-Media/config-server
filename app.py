from mangleconfigs import prepare, match
from json import dumps, load
from flask import Flask, Response, request


app = Flask(__name__)
rules, configs = prepare()

@app.route('/config-server/v1/deliver', methods=['POST'])
def deliver():
    variables = request.get_json()
    config = match(variables, rules)
    return Response(dumps(configs[config].elements), mimetype='application/json')