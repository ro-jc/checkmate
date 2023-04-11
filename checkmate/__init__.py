import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    try:
        SECRET_KEY = open("secret.txt").read()
    except FileNotFoundError:
        SECRET_KEY = "lfskfhslkfh slkajfh"

    app.config.from_mapping(SECRET_KEY=SECRET_KEY, MAX_CONTENT_LENGTH=1 * 1024 * 1024)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/sw.js")
    def service_worker():
        return app.send_static_file("sw.js")

    from checkmate import db

    db.init_app(app)

    from checkmate import auth

    app.register_blueprint(auth.bp)

    from checkmate import views

    app.register_blueprint(views.bp)

    return app


app = create_app()
if __name__ == "__main__":
    app.run()
