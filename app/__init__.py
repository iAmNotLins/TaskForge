from flask import Flask
from .config import Config
from .models.task import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # import routes and register
    from .routes.tasks import bp as tasks_bp
    app.register_blueprint(tasks_bp)
    return app