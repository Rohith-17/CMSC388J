from flask import Blueprint, render_template, redirect, request
from ..forms import ProfessorReviewForm, CurrentProfessorReviewForm
from ..models import LandlordReview
from flask_login import current_user
import numpy as np #use np to find unique values of list

landlords = Blueprint("landlords", __name__)

@landlords.route("/", methods=["GET", "POST"])
def index():
    form = ProfessorReviewForm()
    reviews = ProfessorReview.objects()

    if form.validate_on_submit():
        review = ProfessorReview(
            author = form.name.data,
            landlord_name = form.landlordName.data,
            location = form.address.data,
            rating = form.rating.data,
            review_content = form.landlordReview.data,
            landlord_id = form.landlordName.data.replace(" ", ""))

        review.save()
        return redirect(request.path)
  
    return render_template("index.html", form = form, current_user = current_user, reviews = reviews)

@landlords.route('/landlords/<landlord_id>', methods = ["GET", "POST"])
def landlord(landlord_id):

    form = CurrentProfessorReviewForm()
    #if landlord_name not in database, display a message
    if not ProfessorReview.objects(landlord_id = landlord_id):
        return render_template("index.html")
    
    reviews = ProfessorReview.objects(landlord_id=landlord_id)
    review = reviews.first()
    professor_name = review.landlord_name
    if form.validate_on_submit():
        review = LandlordReview(
            author = form.name.data,
            landlord_name = landlord_name,
            location = form.address.data,
            rating = form.rating.data,
            review_content = form.landlordReview.data,
            landlord_id = form.landlordName.data.replace(" ", ""))

        review.save()
        return redirect(request.path)

    return render_template("landlord.html", reviews=reviews, landlord_name = landlord_name, form = form, current_user = current_user)

#display a list of all of the landlords in the database
@landlords.route('/landlords', methods = ["GET", "POST"])
def landlords_index():

    reviews = ProfessorReview.objects()
    landlord_ids = []
    landlord_names = []
    
    for review in reviews:
        landlord_ids.append(review.landlord_id)
        landlord_names.append(review.landlord_name)

    landlord_ids = list(np.unique(landlord_ids))
    landlord_names = list(np.unique(landlord_names))

    landlords = []
    for i in range(len(landlord_ids)):
        landlords.append((landlord_names[i], landlord_ids[i]))


    #for each id, get all the review ratings for that id

    return render_template("professors_index.html", landlords=landlords,  current_user = current_user)

@landlords.route('/about', methods = ["GET", "POST"])
def about():
    form = ProfessorReviewForm()
 
    return render_template('about.html')
