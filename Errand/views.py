from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from . import db
from .models import  *


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    request = Request.query.all()
    return render_template('home.html', request=request, user=current_user)

@views.route("/create", methods=['POST'])
def create():   
    title = request.form['title']
    description = request.form['description']
    
    request = Request(title=title, description=description, user_id=current_user.id)
    
    db.session.add(request)
    db.session.commit()
    flash('Request Successful!', category='success')
    return redirect(url_for('views.home'))

@views.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)

    if user:
        logout_user()
        db.session.delete(user)
        db.session.commit()

        flash('Your account has been deleted successfully!', category='success')
        return redirect(url_for('auth.login'))
    else:
        flash('User not found', category='error')
        return redirect(url_for('views.home'))
    