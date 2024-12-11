from flask_login import UserMixin
from datetime import datetime
from flask_bcrypt import Bcrypt
from mongoengine import Document, StringField, ReferenceField, DateTimeField, ImageField
from . import db, login_manager


# TODO: implement
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

# TODO: implement fields
class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    email = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField(size=(400, 400, True))

    # Returns unique string identifying our object
    def get_id(self):
        # return str(self.pk)
        return self.username


# TODO: implement fields
class RecipeReview(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(default=datetime.now().strftime("%B %d, %Y at %H:%M:%S"))
    recipe_id = db.StringField(required=True, max_length=50)
    recipe_title = db.StringField(required=True, min_length=1, max_length=100)
    image = db.StringField()
    rating = db.IntField(min_value=1, max_value=5, required=True)