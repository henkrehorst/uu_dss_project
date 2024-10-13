from flask import Blueprint
import json

travelers_compensations_blueprint = Blueprint('travelers_compensations', __name__)


@travelers_compensations_blueprint.route('/travelers_compensations')
def get_travelers_compensations():
    return json.dumps([{
        "id": "compensations",
        "color": "hsl(33, 70%, 50%)",
        "data": [
            {
                "x": "2014",
                "y": 10000
            },
            {
                "x": "2015",
                "y": 20000
            },
            {
                "x": "2016",
                "y": 30000
            },
            {
                "x": "2017",
                "y": 40000
            },
            {
                "x": "2018",
                "y": 50000
            },
            {
                "x": "2019",
                "y": 60000
            },
            {
                "x": "2020",
                "y": 90000
            },
            {
                "x": "2021",
                "y": 30000
            },
            {
                "x": "2022",
                "y": 20000
            },
            {
                "x": "2023",
                "y": 150000
            }
        ]
    }])
