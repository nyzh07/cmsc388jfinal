import base64
import io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import recipe_client
from ..forms import RecipeReviewForm, SearchForm  # Changed to use RecipeReviewForm
from ..models import User, RecipeReview  # Assuming Review model is adapted to work with recipes
from ..utils import current_time

# Changed the blueprint name to 'recipes'
recipes = Blueprint("recipes", __name__)

""" ************ Helper for pictures uses username to get their profile picture ************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """

@recipes.route("/", methods=["GET", "POST"])
def index():
    """Homepage with a search bar for recipes."""
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("recipes.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@recipes.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    """Displays search results for a given query."""
    try:
        # Placeholder: Define the search_recipes function to handle recipe queries
        results = recipe_client.search(query)  
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@recipes.route("/recipe/<recipe_id>", methods=["GET", "POST"])
def recipe_detail(recipe_id):
    """Displays recipe details and allows users to leave reviews."""
    try:
        # Placeholder: Define the retrieve_recipe_by_id function to fetch recipe details
        result = recipe_client.retrieve_recipe_by_id(recipe_id)  
    except ValueError as e:
        return render_template("recipe_detail.html", error_msg=str(e))

    form = RecipeReviewForm()
    if form.validate_on_submit():
        review = RecipeReview(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            recipe_id=recipe_id,  # Use recipe_id
            recipe_title=result.title,  # Use recipe title
            rating=form.rating.data
        )

        review.image = get_b64_img(review.commenter.username)
        review.save()

        return redirect(request.path)

    reviews = RecipeReview.objects(recipe_id=recipe_id)  # Query by recipe_id

    return render_template(
        "recipe_detail.html", form=form, recipe=result, reviews=reviews
    )


@recipes.route("/user/<username>")
def user_detail(username):
    """Displays user details and their reviews."""
    user = User.objects(username=username).first()
    if not user:
        error = f'User "{username}" doesn\'t exist.'
        return render_template("user_detail.html", error=error)
    reviews = RecipeReview.objects(commenter=user)
    image = get_b64_img(user.username)

    return render_template("user_detail.html", user=user, image=image, reviews=reviews)