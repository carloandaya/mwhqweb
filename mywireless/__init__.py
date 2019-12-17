import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DW_DATABASE='DRIVER={SQL Server};SERVER=localhost;DATABASE=MyWirelessDW;Trusted_Connection=yes',
        RAW_DATABASE='DRIVER={SQL Server};SERVER=localhost;DATABASE=MyWirelessRawData;Trusted_Connection=yes',
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

    from . import db
    db.init_app(app)

    from . import mywireless
    app.register_blueprint(mywireless.bp)
    app.add_url_rule('/', endpoint='index')

    from . import data_warehouse
    app.register_blueprint(data_warehouse.bp)
    app.add_url_rule('/data_warehouse', endpoint='index')

    from . import shipment_info
    app.register_blueprint(shipment_info.bp)
    app.add_url_rule('/shipment_info', endpoint='index')

    from . import human_resources
    app.register_blueprint(human_resources.bp)
    app.add_url_rule('/human_resources', endpoint='index')

    return app


app = create_app()
