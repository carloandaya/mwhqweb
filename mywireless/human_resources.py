from pyodbc import IntegrityError
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from mywireless.db import get_db

bp = Blueprint('human_resources', __name__)


@bp.route('/human_resources')
def index():
    return render_template('human_resources/index.html')


@bp.route('/human_resources/employees')
def employees_index():
    employees = get_db().execute(
        'SELECT EmployeeName, '
        'EmployeeKey '
        'FROM DimEmployee'
    ).fetchall()
    return render_template('human_resources/employees/index.html', employees=employees)


@bp.route('/human_resources/assignments')
def assignments_index():
    return render_template('human_resources/assignments/index.html')


# @bp.route('/data_warehouse/categories')
# def categories_index():
#     db = get_db()
#     categories = db.execute(
#         'SELECT CategoryKey, CategoryName'
#         ' FROM DimCategory'
#         ' ORDER BY CategoryName'
#     ).fetchall()
#     return render_template('data_warehouse/categories/index.html', categories=categories)
#
#
# @bp.route('/data_warehouse/categories/create', methods=('GET', 'POST'))
# def categories_create():
#     if request.method == 'POST':
#         category_name = request.form['category_name']
#         db = get_db()
#         error = None
#
#         if not category_name:
#             error = 'Category Name is required.'
#         elif db.execute(
#             'SELECT CategoryName FROM DimCategory where CategoryName = ?', (category_name,)
#         ).fetchone() is not None:
#             error = 'Category Name {} already exists.'.format(category_name)
#
#         if error is not None:
#             flash(error)
#         else:
#             db.execute(
#                 'INSERT INTO DimCategory (CategoryName)'
#                 ' VALUES(?)',
#                 (category_name,)
#             )
#             db.commit()
#             return redirect(url_for('data_warehouse.categories_index'))
#
#     return render_template('data_warehouse/categories/create.html')
#
#
# @bp.route('/data_warehouse/categories/<int:id>/update', methods=('GET', 'POST'))
# def categories_update(id):
#     category = get_category(id)
#
#     if request.method == 'POST':
#         category_name = request.form['category_name']
#         error = None
#
#         if not category_name:
#             error = 'Category Name is required.'
#
#         if error is not None:
#             flash(error)
#         else:
#             try:
#                 db = get_db()
#                 db.execute(
#                     'UPDATE DimCategory'
#                     ' SET CategoryName = ?'
#                     ' WHERE CategoryKey = ?',
#                     (category_name, id)
#                 )
#                 db.commit()
#                 return redirect(url_for('data_warehouse.categories_index'))
#             except IntegrityError:
#                 error = 'Category Name {} already exists.'.format(category_name)
#                 flash(error)
#                 return render_template('data_warehouse/categories/update.html', category=category)
#
#     return render_template('data_warehouse/categories/update.html', category=category)
#
#
# @bp.route('/data_warehouse/manufacturers')
# def manufacturers_index():
#     db = get_db()
#     manufacturers = db.execute(
#         'SELECT ManufacturerKey, ManufacturerName'
#         ' FROM DimManufacturer'
#         ' ORDER BY ManufacturerName'
#     ).fetchall()
#     return render_template('data_warehouse/manufacturers/index.html', manufacturers=manufacturers)
#
#
# @bp.route('/data_warehouse/manufacturers/create', methods=('GET', 'POST'))
# def manufacturers_create():
#     if request.method == 'POST':
#         manufacturer_name = request.form['manufacturer_name']
#         db = get_db()
#         error = None
#
#         if not manufacturer_name:
#             error = 'Manufacturer Name is required.'
#         elif db.execute(
#             'SELECT ManufacturerName FROM DimManufacturer where ManufacturerName = ?', (manufacturer_name,)
#         ).fetchone() is not None:
#             error = 'Manufacturer Name {} already exists.'.format(manufacturer_name)
#
#         if error is not None:
#             flash(error)
#         else:
#             db.execute(
#                 'INSERT INTO DimManufacturer (ManufacturerName)'
#                 ' VALUES(?)',
#                 (manufacturer_name,)
#             )
#             db.commit()
#             return redirect(url_for('data_warehouse.manufacturers_index'))
#
#     return render_template('data_warehouse/manufacturers/create.html')
#
#
# @bp.route('/data_warehouse/manufacturers/<int:id>/update', methods=('GET', 'POST'))
# def manufacturers_update(id):
#     manufacturer = get_manufacturer(id)
#
#     if request.method == 'POST':
#         manufacturer_name = request.form['manufacturer_name']
#         error = None
#
#         if not manufacturer_name:
#             error = 'Manufacturer Name is required.'
#
#         if error is not None:
#             flash(error)
#         else:
#             try:
#                 db = get_db()
#                 db.execute(
#                     'UPDATE DimManufacturer'
#                     ' SET ManufacturerName = ?'
#                     ' WHERE ManufacturerKey = ?',
#                     (manufacturer_name, id)
#                 )
#                 db.commit()
#                 return redirect(url_for('data_warehouse.manufacturers_index'))
#             except IntegrityError:
#                 error = 'Manufacturer Name {} already exists.'.format(manufacturer_name)
#                 flash(error)
#                 return render_template('data_warehouse/manufacturers/update.html', manufacturer=manufacturer)
#
#     return render_template('data_warehouse/manufacturers/update.html', manufacturer=manufacturer)
