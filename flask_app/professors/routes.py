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
            professor_name = form.professorName.data,
            course = form.course.data,
            rating = form.rating.data,
            review_content = form.professorReview.data,
            professor_id = form.professorName.data.replace(" ", ""))

        review.save()
        return redirect(request.path)
  
    return render_template("index.html", form = form, current_user = current_user, reviews = reviews)

@professors.route('/professors/<professor_id>', methods = ["GET", "POST"])
def professor(professor_id):

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
            professor_name = professor_name,
            course = form.course.data,
            rating = form.rating.data,
            review_content = form.professorReview.data,
            professor_id = form.professorName.data.replace(" ", ""))

        review.save()
        return redirect(request.path)

    return render_template("professor.html", reviews=reviews, landlord_name = landlord_name, form = form, current_user = current_user)

#display a list of all of the landlords in the database
@professors.route('/professors', methods = ["GET", "POST"])
def professors_index():

    reviews = ProfessorReview.objects()
    professor_ids = []
    professor_names = []
    
    for review in reviews:
        professor_ids.append(review.professor_id)
        professor_names.append(review.professor_name)

    professor_ids = list(np.unique(landlord_ids))
    professor_names = list(np.unique(landlord_names))

    professors = []
    for i in range(len(professor_ids)):
        professors.append((professor_names[i], professor_ids[i]))


    #for each id, get all the review ratings for that id

    return render_template("professors_index.html", professors=professor,  current_user = current_user)

@landlords.route('/about', methods = ["GET", "POST"])
def about():
    form = ProfessorReviewForm()
 
    return render_template('about.html')
