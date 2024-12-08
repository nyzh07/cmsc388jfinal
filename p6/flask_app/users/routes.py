from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User, RecipeReview

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("movies.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user.save()
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("movies.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and/or password", "danger")

    return render_template("login.html", form=form)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("movies.index"))


# TODO: implement
@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            current_user.username = update_username_form.username.data
            current_user.save()
            flash("Please log in to access this page.", "success")
            logout_user()
            return redirect(url_for("users.login"))

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            picture_file = update_profile_pic_form.picture.data
            current_user.profile_pic.replace(picture_file, content_type=picture_file.content_type)
            current_user.save()
            return redirect(url_for("users.account"))

    if current_user.profile_pic:    
        img_bytes = current_user.profile_pic.read()
        base64_img = base64.b64encode(img_bytes).decode('utf-8')
        image = base64_img
    else:
        image = ""
        
    return render_template("account.html", 
                        update_username_form=update_username_form,
                        update_profile_pic_form=update_profile_pic_form,
                        image=image)


@users.route("/<username>", methods=["GET"])
def user_detail(username):
    # Fetch user by username
    user = User.objects(username=username).first()
    if not user:
        return render_template("user_detail.html", error="User not found")

    # reviews by user
    reviews = RecipeReview.objects(commenter=user)

    # recipes added by the user
    # recipes = Recipe.objects(author=user)

    return render_template(
        "user_detail.html",
        user=user,
        reviews=reviews,
        recipes=[]
    )