import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from .. import recipe_client
from ..forms import RecipeReviewForm, SearchForm
from ..models import User, RecipeReview
from ..utils import current_time
import math

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

    random_recipes = None
    try:
        random_recipes = recipe_client.get_random_recipes()
    except Exception as e:
        print(f"Error fetching random recipes: {e}")

    if form.validate_on_submit():
        return redirect(url_for("recipes.query_results", query=form.search_query.data))

    return render_template("index.html", form=form, random_recipes=random_recipes)


@recipes.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    page = request.args.get('page', 1, type=int)
    try:
        results = recipe_client.search(query, page=page)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    total_results = results["totalResults"]
    total_pages = math.ceil(total_results / 30)
    return render_template("query.html", results=results["results"], query=query, page=page, total_pages=total_pages)


@recipes.route("/recipes/<recipe_id>", methods=["GET", "POST"])
def recipe_detail(recipe_id):
    """Displays recipe details and allows users to leave reviews."""
    try:
        result = recipe_client.get_recipe(recipe_id)  
        if not result:
            return render_template("404.html"), 404
    except Exception as e:
        return render_template("error.html", error_msg=str(e))

    form = RecipeReviewForm()
    if form.validate_on_submit():
        review = RecipeReview(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            recipe_id=recipe_id,
            recipe_title=result.title,
            rating=form.rating.data
        )

        review.image = get_b64_img(review.commenter.username)
        review.save()

        return redirect(request.path)

    reviews = RecipeReview.objects(recipe_id=recipe_id)

    return render_template("recipe_detail.html", form=form, recipe=result, reviews=reviews)

@recipes.route("/user/<username>")
def user_detail(username):
    """Displays user details and their reviews."""
    user = User.objects(username=username).first()
    if not user:
        return render_template("404.html"), 404
    reviews = RecipeReview.objects(commenter=user)
    image = get_b64_img(user.username)

    return render_template("user_detail.html", user=user, image=image, reviews=reviews)



