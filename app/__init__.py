from flask import Flask
from config import Config

# blueprints
from .auth.routes import auth
from .work_order.routes import work_order
from .company.routes import company
from .customer.routes import customer
from .equipment.routes import equipment

# db
from .models import db
from flask_migrate import Migrate

# API CORS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.register_blueprint(auth)
app.register_blueprint(work_order)
app.register_blueprint(company)
app.register_blueprint(customer)
app.register_blueprint(equipment)

app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

from . import routes
from . import models