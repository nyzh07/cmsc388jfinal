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
class Review(db.Document):
    commenter = ReferenceField(User, required=True)
    content = StringField(required=True)
    date = StringField(default=datetime)
    imdb_id = StringField(required=True)
    movie_title = StringField(required=True)
    image = db.StringField()
    #Uncomment when other fields are ready for review pictures