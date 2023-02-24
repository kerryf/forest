from flask import Blueprint, render_template

from forest.guard import login_required

bp = Blueprint('home', __name__)


@bp.get('/home')
@login_required
def index():
    return render_template('home.html')
