from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user
from . import main
from .forms import AddUserForm
from .. import db
from ..models import User


@main.route('/')
def index():
    if current_user.is_anonymous:
        return render_template('index.html', current_user=current_user)
    elif current_user.is_authenticated:
        users = User.query.all()
        return render_template('index.html', users=users, current_user=current_user)


@main.route('/users/add/', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User {user.username} has been added.')
        return redirect(url_for('main.index'))
    return render_template('add_user.html', form=form)


@main.route('/users/remove/<user_id>', methods=['POST'])
def remove_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if request.method == 'POST':
        if user.id != current_user.id:
            db.session.delete(user)
            db.session.commit()
            flash(f"User '{user.username}' has been deleted")
            return redirect(url_for('main.index'))
        else:
            flash(f"You can't delete yourself")
            return redirect(url_for('main.index'))
    else:
        flash(f"Method not allowed")
        return redirect(url_for('main.index'))

