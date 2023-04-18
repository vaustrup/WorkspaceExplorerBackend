from workspaceexplorer import init_app


flask_app = init_app()
celery_app = flask_app.extensions["celery"]

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0")
