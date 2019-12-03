from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from mywireless.db import get_db

bp = Blueprint('shipment_info', __name__)


@bp.route('/')
def index():
    db = get_db()
