import os
from flask import Flask
from mywireless.cache import cache


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='dev',
        DW_DATABASE='DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MyWirelessDW;Trusted_Connection=Yes',
        RAW_DATABASE='DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=MyWirelessRawData;Trusted_Connection=Yes',
        OAUTH_CREDENTIALS={'CLIENT_ID': 'client_id',
                           'CLIENT_SECRET': 'client_secret'},
        OAUTH_PARAMETERS={'REDIRECT_URI': 'http://localhost:5000/login/authorized',
                          'AUTHORITY_URL': 'https://login.microsoftonline.com/common',
                          'AUTH_ENDPOINT': '/oauth2/v2.0/authorize',
                          'TOKEN_ENDPOINT': '/oauth2/v2.0/token',
                          'RESOURCE': 'https://graph.microsoft.com/',
                          'API_VERSION': 'v1.0',
                          'SCOPES': ['User.Read', 'Directory.ReadWrite.All']},
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    cache.init_app(app)

    from . import db
    db.init_app(app)

    with app.app_context():
        from . import mw
        app.register_blueprint(mw.bp)
        app.add_url_rule('/', endpoint='index')

    from . import data_warehouse
    app.register_blueprint(data_warehouse.bp)

    from . import shipment_info
    app.register_blueprint(shipment_info.bp)
    app.add_url_rule('/shipment_info', endpoint='index')

    from . import human_resources
    app.register_blueprint(human_resources.bp)

    return app
