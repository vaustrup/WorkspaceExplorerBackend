from flask import Flask
from flask_cors import CORS
from celery_init import celery_init_app

def init_app(config="config.DevelopmentConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
            task_serializer="pickle",
            accept_content=["pickle"],
            result_accept_content=["json"],
        ),
    )
    #CORS(app)
    
    celery_init_app(app)
    with app.app_context():
        from workspaceexplorer.api import routes
        app.register_blueprint(routes.api_bp)
        return app
