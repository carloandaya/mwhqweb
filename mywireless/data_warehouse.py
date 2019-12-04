from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from mywireless.db import get_db

bp = Blueprint('data_warehouse', __name__)


def get_category(id):
    category = get_db().execute(
        'SELECT CategoryKey, CategoryName'
        ' FROM DimCategory'
        ' WHERE CategoryKey = ?',
        (id,)
    ).fetchone()

    if category is None:
        abort(404, "Category id {0} doesn't exist.".format(id))

    return category


@bp.route('/data_warehouse')
def index():
    return render_template('data_warehouse/index.html')


@bp.route('/data_warehouse/categories')
def categories_index():
    db = get_db()
    categories = db.execute(
        'SELECT CategoryKey, CategoryName'
        ' FROM DimCategory'
        ' ORDER BY CategoryName'
    ).fetchall()
    return render_template('data_warehouse/categories/index.html', categories=categories)


@bp.route('/data_warehouse/categories/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        category_name = request.form['category_name']
        db = get_db()
        error = None

        if not category_name:
            error = 'Category Name is required.'
        elif db.execute(
            'SELECT CategoryName FROM DimCategory where CategoryName = ?', (category_name,)
        ).fetchone() is not None:
            error = 'Category Name {} already exists.'.format(category_name)

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO DimCategory (CategoryName)'
                ' VALUES(?)',
                (category_name,)
            )
            db.commit()
            return redirect(url_for('data_warehouse.categories_index'))

    return render_template('data_warehouse/categories/create.html')


@bp.route('/data_warehouse/categories/<int:id>/update', methods=('GET', 'POST'))
def categories_update(id):
    category = get_category(id)

    if request.method == 'POST':
        category_name = request.form['category_name']
        error = None

        if not category_name:
            error = 'Category Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE DimCategory'
                ' SET CategoryName = ?'
                ' WHERE CategoryKey = ?',
                (category_name, id)
            )
            db.commit()
            return redirect(url_for('data_warehouse.categories_index'))

    return render_template('data_warehouse/categories/update.html', category=category)

