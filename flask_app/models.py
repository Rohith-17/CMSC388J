from flask_login import UserMixin
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    def get_id(self):
        return self.username

class LandlordReview(db.Document, UserMixin):
    author = db.StringField(required=True)
    landlord_name = db.StringField(required=True)
    location = db.StringField(required=True)
    rating = db.IntField(required=True)
    review_content = db.StringField(required=True)
    landlord_id = db.StringField(required=True)
