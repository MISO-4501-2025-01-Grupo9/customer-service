from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSAPI
from config import Config
from .controllers.api import api_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(api_bp, url_prefix="/api")
    db.init_app(app)

    with app.app_context():
        from .models import Customer, CustomerSegment, CustomerSegmentAssignment, CustomerVisit
        db.create_all()

        api = SAFRSAPI(app, host=Config.HOST, port=Config.PORT, prefix="/api")

        # Exponer modelos con métodos CRUD
        api.expose_object(Customer, methods=["GET", "POST", "PATCH", "DELETE"])
        api.expose_object(CustomerSegment, methods=["GET", "POST", "PATCH", "DELETE"])
        api.expose_object(CustomerVisit, methods=["GET", "POST", "PATCH", "DELETE"])
        api.expose_object(CustomerSegmentAssignment, methods=["GET", "POST", "PATCH", "DELETE"])

    return app