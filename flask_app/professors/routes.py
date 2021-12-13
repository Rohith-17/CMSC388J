from flask import Blueprint, render_template, redirect, request
from ..forms import ProfessorReviewForm, CurrentProfessorReviewForm
from ..models import ProfessorReview
from flask_login import current_user
import numpy as np #use np to find unique values of list

professors = Blueprint("professors", __name__)

@professors.route("/", methods=["GET", "POST"])
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
    #if professor_name not in database, display a message
    if not ProfessorReview.objects(professor_id = professor_id):
        return render_template("index.html")
    
    reviews = ProfessorReview.objects(professor_id=professor_id)
    review = reviews.first()
    professor_name = review.professor_name
    if form.validate_on_submit():
        review = ProfessorReview(
            author = form.name.data,
            professor_name = professor_name,
            course = form.course.data,
            rating = form.rating.data,
            review_content = form.professorReview.data,
            professor_id = form.professorName.data.replace(" ", ""))

        review.save()
        return redirect(request.path)

    return render_template("professor.html", reviews=reviews, professor_name = professor_name, form = form, current_user = current_user)

#display a list of all of the professors in the database
@professors.route('/professors', methods = ["GET", "POST"])
def professors_index():

    reviews = ProfessorReview.objects()
    professor_ids = []
    professor_names = []
    
    for review in reviews:
        professor_ids.append(review.professor_id)
        professor_names.append(review.professor_name)

    professor_ids = list(np.unique(professor_ids))
    professor_names = list(np.unique(professor_names))

    professors = []
    for i in range(len(professor_ids)):
        professors.append((professor_names[i], professor_ids[i]))


    #for each id, get all the review ratings for that id

    return render_template("professors_index.html", professors=professor,  current_user = current_user)

@professors.route('/about', methods = ["GET", "POST"])
def about():
    form = ProfessorReviewForm()
 
    return render_template('about.html')
