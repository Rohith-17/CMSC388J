from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from .. import bcrypt
from ..forms import RegisterForm, LoginForm, UpdatePasswordForm, UpdateUsernameForm
from ..models import User

users = Blueprint("users", __name__)

#TODO:
#add more strict password requirements as discussed in specifications
#account html template has to to be fixed, only want to let them change their password or username

@users.route('/users/<username>', methods=['GET', 'POST'])
@login_required
def account(username):
    username_form = UpdateUsernameForm()
    password_form = UpdatePasswordForm()

    if username_form.validate_on_submit():
        print(current_user.username)
        current_user.modify(username=username_form.username.data)
        current_user.save()
        return redirect(url_for('users.account', username=current_user.username))

    if password_form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(password_form.password.data).decode("utf-8")
        current_user.modify(password=hashed)
        current_user.save()
        return redirect(url_for('users.account', username=current_user.username))

    return render_template('account.html', username_form=username_form, password_form=password_form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('professors.index'))
    
    form = LoginForm()
    errors = ""
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        print("entering form validation")
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            print("here")
            login_user(user)
            return redirect(url_for('users.account', username=form.username.data))
        else:
            flash("Login Failed. Make sure you entered the right username/password")
            errors = "Login Failed. Make sure you entered the right username/password"
            print("errors is being updated to ", errors)
    return render_template('login.html', form=form, errors=errors)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()

        return redirect(url_for("users.login"))


    return render_template('register.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('professors.index'))
