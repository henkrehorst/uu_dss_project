from flask import Blueprint
import json

performance_blueprint = Blueprint('performance', __name__)


@performance_blueprint.route('/performance/tsb')
def performance_tsb():
    return json.dumps({
        'value': 73
    })


@performance_blueprint.route('/performance/equipment')
def performance_equipment():
    return json.dumps({
        'value': 45
    })


@performance_blueprint.route('/performance/infrastructure')
def performance_infrastructure():
    return json.dumps({
        'value': 20
    })
