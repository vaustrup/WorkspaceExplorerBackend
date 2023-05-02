import os
from werkzeug.middleware.proxy_fix import ProxyFix

from flask import Flask
from flask_cors import CORS
from celery_init import celery_init_app


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

def init_app(config="config.DevelopmentConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=CELERY_BROKER_URL,
            result_backend=CELERY_RESULT_BACKEND,
            task_ignore_result=True,
            task_serializer="pickle",
            accept_content=["pickle"],
            result_accept_content=["json"],
        ),
    )
    
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    celery_init_app(app)
    with app.app_context():
        from workspaceexplorer.api import routes
        app.register_blueprint(routes.api_bp)
        return app
