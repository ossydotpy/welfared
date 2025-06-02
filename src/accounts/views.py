from flask import Blueprint, flash, redirect, render_template, url_for
from src import app
from src.accounts.forms import RegisterForm, LoginForm
from src.accounts.repo import register as register_fn, login as login_fn
accounts_bp = Blueprint('accounts', __name__)



@accounts_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            register_fn(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data,
                password=form.password.data
            )
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('accounts.login'))
        except ValueError as ve:
            app.logger.warning(f"Validation error: {ve}")
            flash(str(ve), 'warning')
        except Exception as e:
            app.logger.error(f"Unexpected error: {e}")
            flash('Something went wrong. Please try again.', 'danger')
    
    return render_template('accounts/register.html', form=form)

@accounts_bp.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            login_fn(
                phone=form.phone.data,
                password=form.password.data
            )
            return redirect(url_for('core.index'))
        except ValueError as e:
            flash('Wrong phone or password, try again')
        except Exception as e:
            flash('An error occured', 'danger')
            app.logger.error(e, with_traceback=True)
    return render_template('accounts/login.html', form=form)