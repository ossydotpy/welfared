from flask import Blueprint, render_template_string
from flask_login import current_user


core_bp = Blueprint('core', __name__)

@core_bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template_string('<h1>Hello {{ user.first_name }}</h1>', user=current_user)
    return render_template_string('<h1>home</>')