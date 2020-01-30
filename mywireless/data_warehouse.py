from pyodbc import IntegrityError
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length


from mywireless.db import get_db

bp = Blueprint('data_warehouse', __name__, url_prefix='/data_warehouse')


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


def get_location(id):
    location = get_db().execute(
        'SELECT s.StoreKey, s.StoreName, r.RegionKey, r.RegionName, s.DealerCode, s.RQAbbreviation, s.IsActive'
        ' FROM DimStore s JOIN DimRegion r ON s.RegionKey = r.RegionKey'
        ' WHERE s.StoreKey = ?',
        (id,)
    ).fetchone()

    if location is None:
        abort(404, "Location id {0} doesn't exist.".format(id))

    return location


def get_location_district(id):
    location_district = get_db().execute(
        'SELECT s.StoreName, d.DistrictName, a.StartDate, a.EndDate'
        ' FROM DimStoreAssignment a JOIN DimStore s ON a.StoreKey = s.StoreKey' 
        ' JOIN DimDistrict d ON a.DistrictKey = d.DistrictKey'
        ' WHERE a.StoreKey = ?'
        ' ORDER BY a.StartDate DESC', id
    )

    return location_district


def get_manufacturer(id):
    manufacturer = get_db().execute(
        'SELECT ManufacturerKey, ManufacturerName'
        ' FROM DimManufacturer'
        ' WHERE ManufacturerKey = ?',
        (id,)
    ).fetchone()

    if manufacturer is None:
        abort(404, "Manufacturer id {0} doesn't exist.".format(id))

    return manufacturer


@bp.route('/')
def index():
    return render_template('data_warehouse/index.html')


@bp.route('/categories')
def categories_index():
    db = get_db()
    categories = db.execute(
        'SELECT CategoryKey, CategoryName'
        ' FROM DimCategory'
        ' ORDER BY CategoryName'
    ).fetchall()
    return render_template('data_warehouse/categories/index.html', categories=categories)


@bp.route('/categories/create', methods=('GET', 'POST'))
def categories_create():
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


@bp.route('/categories/<int:id>/update', methods=('GET', 'POST'))
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
            try:
                db = get_db()
                db.execute(
                    'UPDATE DimCategory'
                    ' SET CategoryName = ?'
                    ' WHERE CategoryKey = ?',
                    (category_name, id)
                )
                db.commit()
                return redirect(url_for('data_warehouse.categories_index'))
            except IntegrityError:
                error = 'Category Name {} already exists.'.format(category_name)
                flash(error)
                return render_template('data_warehouse/categories/update.html', category=category)

    return render_template('data_warehouse/categories/update.html', category=category)


class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dealer_code = StringField('Dealer Code')
    rq_abbreviation = StringField('RQ Abbreviation')
    is_active = BooleanField('Is Active')
    region = SelectField('Region', coerce=int)


@bp.route('/locations')
def locations_index():
    db = get_db()
    locations = db.execute(
        'SELECT s.StoreKey, s.StoreName, r.RegionName, s.DealerCode, s.RQAbbreviation'
        ' FROM DimStore s JOIN DimRegion r'
        ' ON s.RegionKey = r.RegionKey'
        ' WHERE s.IsActive = 1'
        ' ORDER BY s.StoreName'
    ).fetchall()
    return render_template('data_warehouse/locations/index.html', locations=locations)


@bp.route('/locations/<int:id>')
def locations_detail(id):
    location = get_location(id)
    district = get_location_district(id)
    return render_template('data_warehouse/locations/detail.html', location=location, district=district)


@bp.route('/locations/create', methods=('GET', 'POST'))
def locations_create():
    db = get_db()
    regions = db.execute(
        'SELECT RegionKey, RegionName'
        ' FROM DimRegion'
    ).fetchall()
    regions_select = [(r.RegionKey, r.RegionName) for r in regions]
    form = LocationForm()
    form.region.choices = regions_select
    form.is_active.data = True

    if form.validate_on_submit():
        db.execute(
            'INSERT INTO DimStore (StoreName, RegionKey, DealerCode, RQAbbreviation, IsActive)'
            ' VALUES(?, ?, ?, ?, ?)',
            (form.name.data, form.region.data, form.dealer_code.data, form.rq_abbreviation.data, form.is_active.data)
        )
        db.commit()
        return redirect(url_for('data_warehouse.locations_index'))

    return render_template('data_warehouse/locations/create_update.html', form=form)


@bp.route('/locations/<int:id>/update', methods=('GET', 'POST'))
def locations_update(id):
    db = get_db()
    regions = db.execute(
        'SELECT RegionKey, RegionName'
        ' FROM DimRegion'
    ).fetchall()
    regions_select = [(r.RegionKey, r.RegionName) for r in regions]
    form = LocationForm()
    form.region.choices = regions_select

    if form.validate_on_submit():
        try:
            db.execute(
                'UPDATE DimStore'
                ' SET StoreName = ?, RegionKey = ?, DealerCode = ?, RQAbbreviation = ?'
                ' WHERE StoreKey = ? ',
                (form.name.data, form.region.data, form.dealer_code.data, form.rq_abbreviation.data, id)
            )
            db.commit()
            return redirect(url_for('data_warehouse.locations_index'))
        except IntegrityError:
            error = 'Store Name {} already exists.'.format(form.name.data)
            flash(error)
            return render_template('data_warehouse/locations/update.html', form=form)

    location = db.execute(
        'SELECT StoreKey, StoreName, RegionKey, DealerCode, RQAbbreviation, IsActive'
        ' FROM DimStore'        
        ' WHERE StoreKey = ?', id
    ).fetchone()

    form.name.data = location.StoreName
    form.region.data = location.RegionKey
    form.dealer_code.data = location.DealerCode
    form.rq_abbreviation.data = location.RQAbbreviation
    form.is_active.data = location.IsActive

    return render_template('data_warehouse/locations/create_update.html', form=form)


@bp.route('/manufacturers')
def manufacturers_index():
    db = get_db()
    manufacturers = db.execute(
        'SELECT ManufacturerKey, ManufacturerName'
        ' FROM DimManufacturer'
        ' ORDER BY ManufacturerName'
    ).fetchall()
    return render_template('data_warehouse/manufacturers/index.html', manufacturers=manufacturers)


@bp.route('/manufacturers/create', methods=('GET', 'POST'))
def manufacturers_create():
    if request.method == 'POST':
        manufacturer_name = request.form['manufacturer_name']
        db = get_db()
        error = None

        if not manufacturer_name:
            error = 'Manufacturer Name is required.'
        elif db.execute(
            'SELECT ManufacturerName FROM DimManufacturer where ManufacturerName = ?', (manufacturer_name,)
        ).fetchone() is not None:
            error = 'Manufacturer Name {} already exists.'.format(manufacturer_name)

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO DimManufacturer (ManufacturerName)'
                ' VALUES(?)',
                (manufacturer_name,)
            )
            db.commit()
            return redirect(url_for('data_warehouse.manufacturers_index'))

    return render_template('data_warehouse/manufacturers/create.html')


@bp.route('/manufacturers/<int:id>/update', methods=('GET', 'POST'))
def manufacturers_update(id):
    manufacturer = get_manufacturer(id)

    if request.method == 'POST':
        manufacturer_name = request.form['manufacturer_name']
        error = None

        if not manufacturer_name:
            error = 'Manufacturer Name is required.'

        if error is not None:
            flash(error)
        else:
            try:
                db = get_db()
                db.execute(
                    'UPDATE DimManufacturer'
                    ' SET ManufacturerName = ?'
                    ' WHERE ManufacturerKey = ?',
                    (manufacturer_name, id)
                )
                db.commit()
                return redirect(url_for('data_warehouse.manufacturers_index'))
            except IntegrityError:
                error = 'Manufacturer Name {} already exists.'.format(manufacturer_name)
                flash(error)
                return render_template('data_warehouse/manufacturers/update.html', manufacturer=manufacturer)

    return render_template('data_warehouse/manufacturers/update.html', manufacturer=manufacturer)
