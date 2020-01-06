from pyodbc import IntegrityError
from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from mywireless.mw import hr_login_required

from mywireless.db import get_db


class EmployeeCreateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    initials = StringField('Initials', validators=[DataRequired(),
                                                   Length(min=2,
                                                          max=2,
                                                          message='Field must be exactly 2 characters long.')])


class EmployeeUpdateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    att_uid = StringField('ATTUID')


bp = Blueprint('human_resources', __name__, url_prefix='/human_resources')


def get_employee(id):
    employee = get_db().execute(
        'SELECT EmployeeKey, EmployeeName, ATTUID, Email'
        ' FROM DimEmployee'
        ' WHERE EmployeeKey = ?',
        (id,)
    ).fetchone()

    if employee is None:
        abort(404, "Employee id {0} doesn't exist.".format(id))

    return employee


@bp.route('/')
def index():
    return render_template('human_resources/index.html')


@bp.route('/employees')
def employees_index():
    employees = get_db().execute(
        'SELECT EmployeeName, '
        'EmployeeKey, '
        'Email '
        'FROM DimEmployee'
    ).fetchall()
    return render_template('human_resources/employees/index.html', employees=employees)


@bp.route('/employees/<int:id>')
def employees_detail(id):
    employee = get_employee(id)
    return render_template('human_resources/employees/employee.html', employee=employee)


@bp.route('/employees/create', methods=('GET', 'POST'))
@hr_login_required
def employees_create():
    db = get_db()
    form = EmployeeCreateForm()
    if form.validate_on_submit():
        new_employee = db.execute(
            'INSERT INTO DimEmployee (EmployeeName)'
            ' OUTPUT INSERTED.EmployeeKey, INSERTED.EmployeeName'
            ' VALUES (?)',
            form.name.data
        ).fetchone()
        db.commit()
        employee = {'EmployeeKey': new_employee[0], 'EmployeeName': new_employee[1]}
        email_address = db.execute(
            'UPDATE DimEmployee '
            'SET Email = ? '            
            'OUTPUT INSERTED.Email '
            'WHERE EmployeeKey = ? ',
            (str(form.initials.data).lower() + str(employee['EmployeeKey']) + '@mywirelessgroup.com'
             , employee['EmployeeKey'])
        ).fetchone()[0]
        db.commit()
        employee['Email'] = email_address
        return redirect(url_for('human_resources.employees_detail', id=employee['EmployeeKey']))
    return render_template('human_resources/employees/create.html', form=form)


@bp.route('/employees/<int:id>/update', methods=('GET', 'POST'))
@hr_login_required
def employees_update(id):
    employee = get_employee(id)
    form = EmployeeUpdateForm()
    form.name.data = employee[1]
    form.att_uid.data = employee[2]

    if form.validate_on_submit():
        employee_name = request.form['name']
        employee_attuid = request.form['att_uid']
        print(employee_name)
        print(employee_attuid)
        error = None

        if not employee_name:
            error = 'Employee Name is required.'

        if error is not None:
            flash(error)
        else:
            try:
                db = get_db()
                db.execute(
                    'UPDATE DimEmployee'
                    ' SET EmployeeName = ?, ATTUID = ?'
                    ' WHERE EmployeeKey = ?',
                    (employee_name, employee_attuid, id)
                )
                db.commit()
                return redirect(url_for('human_resources.employees_index'))
            except IntegrityError:
                error = 'ATTUID {} already exists.'.format(employee_attuid)
                flash(error)
                return render_template('human_resources/employees/update.html', form=form)

    return render_template('human_resources/employees/update.html', form=form)


@bp.route('/assignments')
def assignments_index():
    return render_template('human_resources/assignments/index.html')
