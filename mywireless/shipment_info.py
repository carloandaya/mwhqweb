from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from mywireless.db import get_db_raw

bp = Blueprint('shipment_info', __name__)


def get_delivered_not_received():
    shipments = get_db_raw().execute(
        'SELECT PONumber, ActualShipDate, ItemNumber, ItemDescription,'
        ' ExtdPrice, QuantityShipped, IMEI, TrackingNumber'
        ' FROM ATT_ShipmentDetailReport'
        ' WHERE DeliveryStatus = ? AND IsReceived = ?',
        ('D', 0)
    ).fetchall()
    return shipments


@bp.route('/shipment_info')
def index():
    return render_template('shipment_info/index.html')


@bp.route('/shipment_info/shipped_not_received')
def shipped_not_received():
    db = get_db_raw()
    shipments = db.execute(
        'SELECT PONumber, ActualShipDate, ItemNumber, ItemDescription,'
        ' ExtdPrice, QuantityShipped, IMEI, TrackingNumber'
        ' FROM ATT_ShipmentDetailReport'
        ' WHERE IsReceived = ?',
        0
    ).fetchall()
    return render_template('shipment_info/shipped_not_received.html', shipments=shipments)


@bp.route('/shipment_info/shipped_not_delivered')
def shipped_not_delivered():
    db = get_db_raw()
    shipments = db.execute(
        'SELECT PONumber, ActualShipDate, ItemNumber, ItemDescription,'
        ' ExtdPrice, QuantityShipped, IMEI, TrackingNumber'
        ' FROM ATT_ShipmentDetailReport'
        ' WHERE DeliveryStatus != ? OR DeliveryStatus IS NULL',
        'D'
    ).fetchall()
    return render_template('shipment_info/shipped_not_delivered.html', shipments=shipments)


@bp.route('/shipment_info/delivered_not_received')
def delivered_not_received():
    shipments = get_delivered_not_received()
    return render_template('shipment_info/delivered_not_received.html', shipments=shipments)
