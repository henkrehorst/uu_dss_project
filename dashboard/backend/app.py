from flask import Flask
from flask_cors import CORS
from routes.rail_routes import rail_routes_blueprint
from routes.performance import performance_blueprint
from routes.travelers_compensations import travelers_compensations_blueprint
from dotenv import load_dotenv

# Load env variables
load_dotenv('.env')

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

app.register_blueprint(rail_routes_blueprint)
app.register_blueprint(performance_blueprint)
app.register_blueprint(travelers_compensations_blueprint)


if __name__ == '__main__':
    app.run(debug=True)