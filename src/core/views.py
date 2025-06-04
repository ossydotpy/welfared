from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from src.models import User, Group, GroupMember, WelfarePayment, WelfarePaymentTransaction
from src.core.forms import CreateWelfareGroupForm
from src import db

core_bp = Blueprint('core', __name__)

@core_bp.route('/')
def index():
    return render_template('core/index.html')

@core_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('core/dashboard.html')


@core_bp.route('dashboard/groups')
@login_required
def admin_groups():
    groups = Group.query.filter_by(owner_id=current_user.get_id()).all()
    return render_template('core/admin_groups.html', groups=groups)


@core_bp.route('/dashboard/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateWelfareGroupForm()
    if form.validate_on_submit():
        new_group = Group(name=form.name.data, owner_id=current_user.get_id())
        db.session.add(new_group)
        db.session.commit()
        return redirect(url_for('core.admin_groups'))

    return render_template('core/create_group.html', form=form)

@core_bp.route('/dashboard/groups/<int:group_id>/delete', methods=['DELETE'])
@login_required
def delete_group(group_id):
    group = db.session.get(Group, group_id)
    if not group:
        flash('Group not found', 'error')
        return redirect(url_for('core.admin_groups'))

    if group.owner_id != int(current_user.get_id()):
        flash('You are not authorized to delete this group', 'error')
        return redirect(url_for('core.admin_groups'))

    try:
        db.session.delete(group)
        db.session.commit()
        flash('Group deleted successfully', 'success')
    except Exception as e:
        logging.exception('Error deleting group')
        db.session.rollback()
        flash('An error occurred while deleting the group', 'error')

    return redirect(url_for('core.admin_groups'))