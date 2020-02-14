from pyodbc import IntegrityError
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, jsonify)
from werkzeug.exceptions import abort
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length
from mywireless import cache
from mywireless.mw import po_login_required
import datetime
import time

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
        'SELECT s.StoreKey, s.StoreName, s.RegionKey, s.DealerCode, s.RQAbbreviation, s.IsActive, a.DistrictKey'        
        ' FROM DimStore s JOIN DimRegion r ON s.RegionKey = r.RegionKey'
        ' LEFT JOIN DimStoreAssignment a on s.StoreKey = a.StoreKey AND a.EndDate IS NULL'        
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


def get_product(id):
    product = get_db().execute(
        'SELECT ManufacturerKey, CategoryKey, ProductName, SubcategoryKey'
        ' FROM DimProduct'
        ' WHERE ProductKey = ?',
        (id)
    ).fetchone()

    if product is None:
        abort(404, "Product SKU {} doesn't exist.".format(id))

    return product


@cache.cached(timeout=300, key_prefix='all_products')
def get_products():
    products = get_db().execute(
        'SELECT p.ProductKey, m.ManufacturerName, c.CategoryName, p.ProductName, s.SubcategoryName'
        ' FROM DimProduct p '
        ' LEFT JOIN DimManufacturer m on p.ManufacturerKey = m.ManufacturerKey'
        ' LEFT JOIN DimCategory c on p.CategoryKey = c.CategoryKey'
        ' LEFT JOIN DimSubcategory s on p.SubcategoryKey = s.SubcategoryKey'
    ).fetchall()

    return products


@cache.cached(timeout=300, key_prefix='products_no_manufacturer')
def get_products_no_manufacturer():
    products = get_db().execute(
        'SELECT p.ProductKey, m.ManufacturerName, c.CategoryName, p.ProductName, s.SubcategoryName'
        ' FROM DimProduct p '
        ' LEFT JOIN DimManufacturer m on p.ManufacturerKey = m.ManufacturerKey'
        ' LEFT JOIN DimCategory c on p.CategoryKey = c.CategoryKey'
        ' LEFT JOIN DimSubcategory s on p.SubcategoryKey = s.SubcategoryKey'
        ' WHERE p.ManufacturerKey = -1'
    ).fetchall()

    return products


@bp.route('/')
def index():
    db = get_db()
    product_no_manufacturer = db.execute(
        'SELECT ProductKey'
        ' FROM DimProduct'
        ' WHERE ManufacturerKey = -1'
    ).fetchone()
    no_manufacturer = product_no_manufacturer
    return render_template('data_warehouse/index.html', no_manufacturer=no_manufacturer)


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
    district = SelectField('District', coerce=int)
    district_startdate = DateField('District Start Date', render_kw={'placeholder': 'YYYY-MM-DD'})


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


@bp.route('/locations/districts/<int:region>')
def district(region):
    db = get_db()
    districts = db.execute(
        'SELECT DistrictKey, DistrictName'
        ' FROM DimDistrict'
        ' WHERE RegionKey = ?',
        region
    ).fetchall()

    dis_array = []
    for d in districts:
        dis_obj = dict()
        dis_obj['id'] = d.DistrictKey
        dis_obj['name'] = d.DistrictName
        dis_array.append(dis_obj)

    return jsonify({'districts': dis_array})


@bp.route('/locations/<int:id>/update', methods=('GET', 'POST'))
def locations_update(id):
    db = get_db()
    location = get_location(id)
    form = LocationForm()
    regions = db.execute(
        'SELECT RegionKey, RegionName'
        ' FROM DimRegion'
    ).fetchall()
    regions_select = [(r.RegionKey, r.RegionName) for r in regions]

    if request.method == 'POST':
        districts = db.execute(
            'SELECT DistrictKey, DistrictName'
            ' FROM DimDistrict'
            ' WHERE RegionKey = ?',
            form.region.data
        ).fetchall()
    else:
        districts = db.execute(
            'SELECT DistrictKey, DistrictName'
            ' FROM DimDistrict'
            ' WHERE RegionKey = ?',
            location.RegionKey
        ).fetchall()

    districts_select = [(d.DistrictKey, d.DistrictName) for d in districts]

    form.region.choices = regions_select
    form.district.choices = districts_select

    if form.validate_on_submit():
        location_district = db.execute(
            'SELECT DistrictKey FROM DimStoreAssignment WHERE StoreKey = ? AND EndDate IS NULL',
            id
        ).fetchone()
        try:
            db.execute(
                'UPDATE DimStore'
                ' SET StoreName = ?, RegionKey = ?, DealerCode = ?, RQAbbreviation = ?, IsActive = ?'
                ' WHERE StoreKey = ? ',
                (form.name.data, form.region.data, form.dealer_code.data, form.rq_abbreviation.data,
                 form.is_active.data, id)
            )
            db.commit()

            if (location_district is None or form.district.data != location_district.DistrictKey) \
                    and form.district_startdate.data:
                print(form.district_startdate.data)
                print(type(form.district_startdate.data))
                db.execute(
                    'INSERT INTO DimStoreAssignment (StoreKey, DistrictKey, StartDate)'
                    ' VALUES (?, ?, ?)',
                    (id, form.district.data, form.district_startdate.data)
                )
                db.commit()

            return redirect(url_for('data_warehouse.locations_index'))
        except IntegrityError:
            error = 'Store Name {} already exists.'.format(form.name.data)
            flash(error)
            return render_template('data_warehouse/locations/create_update.html', form=form)

    location = db.execute(
        'SELECT s.StoreKey, s.StoreName, s.RegionKey, s.DealerCode, s.RQAbbreviation, s.IsActive, a.DistrictKey'
        ' FROM DimStore s LEFT JOIN DimStoreAssignment a ON s.StoreKey = a.StoreKey AND a.EndDate IS NULL'            
        ' WHERE s.StoreKey = ?', id
    ).fetchone()

    form.name.data = location.StoreName
    form.region.data = location.RegionKey
    form.dealer_code.data = location.DealerCode
    form.rq_abbreviation.data = location.RQAbbreviation
    form.is_active.data = location.IsActive

    return render_template('data_warehouse/locations/create_update.html', form=form)


class ProductForm(FlaskForm):
    product_name = StringField('Product Name')
    manufacturer_key = SelectField('Manufacturer Key', coerce=int)
    category_key = SelectField('Category', coerce=int)
    subcategory_key = SelectField('Subcategory', coerce=int)


@bp.route('/maintenance/products-no-manufacturer')
@po_login_required
def products_no_manufacturer_index():
    products = get_products_no_manufacturer()
    return render_template('data_warehouse/products/index.html', products=products)


@bp.route('/products')
def products_index():
    products = get_products()
    return render_template('data_warehouse/products/index.html', products=products)


@bp.route('/products/subcategory/<int:category>')
def subcategory(category):
    db = get_db()
    subcategories = db.execute(
        'SELECT SubcategoryKey, SubcategoryName'
        ' FROM DimSubcategory'
        ' WHERE CategoryKey = ?',
        category
    ).fetchall()

    sub_array = []
    for s in subcategories:
        sub_obj = dict()
        sub_obj['id'] = s.SubcategoryKey
        sub_obj['name'] = s.SubcategoryName
        sub_array.append(sub_obj)

    return jsonify({'subcategories': sub_array})


@bp.route('/products/<id>/update', methods=('GET', 'POST'))
def products_update(id):
    product = get_product(id)
    db = get_db()
    form = ProductForm()

    manufacturers = db.execute(
        'SELECT ManufacturerKey, ManufacturerName'
        ' FROM DimManufacturer'
    ).fetchall()
    categories = db.execute(
        'SELECT CategoryKey, CategoryName'
        ' FROM DimCategory'
    ).fetchall()

    if request.method == 'POST':
        subcategories = db.execute(
            'SELECT SubcategoryKey, SubcategoryName'
            ' FROM DimSubcategory'
            ' WHERE CategoryKey = ?',
            form.category_key.data
        ).fetchall()
    else:
        subcategories = db.execute(
            'SELECT SubcategoryKey, SubcategoryName'
            ' FROM DimSubcategory'
            ' WHERE CategoryKey = ?',
            product.CategoryKey
        ).fetchall()

    manufacturers_select = [(m.ManufacturerKey, m.ManufacturerName) for m in manufacturers]
    categories_select = [(c.CategoryKey, c.CategoryName) for c in categories]
    subcategories_select = [(s.SubcategoryKey, s.SubcategoryName) for s in subcategories]

    form.manufacturer_key.choices = manufacturers_select
    form.category_key.choices = categories_select
    form.subcategory_key.choices = subcategories_select

    if form.validate_on_submit():
        try:
            db.execute(
                'UPDATE DimProduct'
                ' SET ManufacturerKey = ?, CategoryKey = ?, ProductName = ?, SubcategoryKey = ?'
                ' WHERE ProductKey = ?',
                (form.manufacturer_key.data, form.category_key.data, form.product_name.data, form.subcategory_key.data, id)
            )
            db.commit()
            error = 'Updated product {}: {}.'.format(id, form.product_name.data)
            flash(error)
            cache.clear()
            return redirect(url_for('data_warehouse.index'))
        except IntegrityError:
            error = 'Store Name {} already exists.'.format(form.name.data)
            flash(error)
            return render_template('data_warehouse/locations/update.html', form=form)

    form.manufacturer_key.data = product.ManufacturerKey
    form.category_key.data = product.CategoryKey
    form.product_name.data = product.ProductName
    form.subcategory_key.data = product.SubcategoryKey if product.SubcategoryKey else None
    return render_template('data_warehouse/products/update.html', form=form)


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
