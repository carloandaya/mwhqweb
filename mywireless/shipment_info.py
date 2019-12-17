from pyodbc import IntegrityError
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from mywireless.db import get_db_raw

bp = Blueprint('shipment_info', __name__)


def get_shipment(id):
    shipment = get_db_raw().execute(
        'SELECT IMEI, '
        'DeliveryStatus '
        'FROM ATT_ShipmentDetailReport '
        'WHERE IMEI = ?',
        id
    ).fetchone()

    if shipment is None:
        abort(404, "Shipment with IMEI {0} doesn't exist.".format(id))

    return shipment


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


@bp.route('/shipment_info/imei/<id>/update')
def update_by_imei(id):
    shipment = get_shipment(id)

    if request.method == 'POST':
        delivery_status = request.form['delivery_status']
        error = None

        if not delivery_status:
            delivery_status = None

        db = get_db_raw()
        db.execute(
            'UPDATE ATT_ShipmentDetailReport'
            ' SET DeliveryStatus = ?'
            ' WHERE IMEI = ?',
            (delivery_status, id)
        )
        db.commit()
        return redirect(url_for('shipment_info.index'))

    return render_template('shipment_info/update_by_imei.html', shipment=shipment)
