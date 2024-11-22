from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


# User Model
class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True, min_length=1, max_length=40)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()

    def get_id(self):
        return self.username


# Recipe Review Model
class RecipeReview(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(default=datetime.now().strftime("%B %d, %Y at %H:%M:%S"))
    recipe_id = db.StringField(required=True, max_length=50)  # Recipe identifier
    recipe_title = db.StringField(required=True, min_length=1, max_length=100)
    image = db.StringField()  # Optional image field for reviews, like a user-uploaded image for the review
    rating = db.IntField(min_value=1, max_value=5, required=True)