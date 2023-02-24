from flask import Blueprint, render_template

from forest.guard import guest_required

bp = Blueprint('forest', __name__)


@bp.get('/')
@guest_required
def index():
    return render_template('index.html')
