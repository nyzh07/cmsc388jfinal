import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from .. import recipe_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time

recipes = Blueprint("recipes", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """


@recipes.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("recipes.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@recipes.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = recipe_client.search(query)
        
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results["results"])


@recipes.route("/recipes/<recipe_id>", methods=["GET", "POST"])
def recipe_detail(recipe_id):
    try:
        result = recipe_client.get_recipe(recipe_id)
    except ValueError as e:
        return render_template("recipe_detail.html", error_msg=str(e))
    
    form = MovieReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=recipe_id,
            movie_title=result.title,
        )
        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=recipe_id)

    return render_template(
        "recipe_detail.html", recipe=result
    )



