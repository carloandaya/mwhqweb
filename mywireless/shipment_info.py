from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from mywireless.db import get_db_raw

bp = Blueprint('shipment_info', __name__)


@bp.route('/shipment_info')
def index():
    return render_template('shipment_info/index.html')


@bp.route('/shipment_info/shipped_not_received')
def shipped_not_received():
    db = get_db_raw()
    shipments = db.execute(
        'SELECT PONumber, ActualShipDate, ItemNumber, ItemDescription,'
        ' ExtdPrice, QuantityiShipped, IMEI, TrackingNumber'
        ' FROM ATT_ShipmentDetailReport'
        ' WHERE IsReceived = 0'
    ).fetchall()
    return render_template('shipment_info/shipped_not_received.html', shipments=shipments)


@bp.route('/shipment_info/delivered_not_received')
def delivered_not_received():
    db = get_db_raw()
    shipments = db.execute(
        'SELECT PONumber, ActualShipDate, ItemNumber, ItemDescription,'
        ' ExtdPrice, QuantityiShipped, IMEI, TrackingNumber'
        ' FROM ATT_ShipmentDetailReport'
        ' WHERE DeliveryStatus = "D" AND IsReceived = 0'
    ).fetchall()
    return render_template('shipment_info/delivered_not_received.html', shipments=shipments)
