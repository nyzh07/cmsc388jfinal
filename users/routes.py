from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User
from ..recipes.routes import get_b64_img


users = Blueprint("users", __name__)

""" ************ User Management views ************ """


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
     #Check if authenticated
    if current_user.is_authenticated:
        return redirect(url_for('recipess.index'))
    
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        )
        user.save()
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    loginForm = LoginForm()
    #Check if authenticated
    if current_user.is_authenticated:
        return redirect(url_for('recipes.index'))

    if loginForm.validate_on_submit():
        user = User.objects(username=loginForm.username.data).first()
        
        if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
            login_user(user)
            return redirect(url_for('users.account'))
        else:
            flash("Login failed. Check your username and/or password", "danger")
    
    return render_template('login.html', form=loginForm)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('recipes.index'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    image = None

    if request.method == "POST":
        # Update username
        if update_username_form.submit_username.data and update_username_form.validate():
            current_user.username = update_username_form.username.data  # Corrected variable name
            current_user.save()
            flash("Username updated successfully.")
            return redirect(url_for('users.account'))

        # Update profile picture
        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            pic = update_profile_pic_form.picture.data  # Corrected variable name
            current_user.profile_pic.put(pic, content_type=pic.content_type)
            current_user.save()
            flash("Profile picture updated successfully.")
            return redirect(url_for('users.account'))
    else:
           # Load the current user's profile picture for GET requests
        image = get_b64_img(current_user.username) if current_user.profile_pic else None

    return render_template("account.html",
                           update_username_form=update_username_form, 
                           update_profile_pic_form=update_profile_pic_form, 
                           image=image)