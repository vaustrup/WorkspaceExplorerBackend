from workspaceexplorer import init_app


application = init_app()
celery_app = flask_app.extensions["celery"]

if __name__ == "__main__":
    application.run(host="0.0.0.0")
