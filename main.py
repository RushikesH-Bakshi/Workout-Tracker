from flask import Blueprint, flash, render_template, url_for, request, redirect, send_file
from flask_login import login_required, current_user
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    from .models import User, Workout
    from . import db
except ImportError:
    from models import User, Workout
    from __init__ import db

main = Blueprint("main", __name__)

@main.route('/')
def home():
    return redirect('./pages/index.js')

@main.route('/api/profile')
@login_required
def profile():
    return redirect('./pages/_app.js', name=current_user.name)

@main.route('/api/newWorkout', methods=['GET', 'POST'])
@login_required
def new_workout():
    if request.method == 'GET':
        return render_template('create_new_workout.html')
    
    if request.method == 'POST':
        count = request.form.get('count')
        comment = request.form.get('comment')
        workout = Workout(count=count, comment=comment, author=current_user)

        db.session.add(workout)
        db.session.commit()
        
        flash("Your workout has been added")
        return redirect(url_for('main.get_workouts'))
    
@main.route('/api/getWorkouts', methods=['GET'])
@login_required
def get_workouts():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    pushup = Workout.query.filter_by(author=current_user).paginate(page=page, per_page=6)
    return render_template("all_workouts.html", user=user, workouts=pushup)

@main.route('/api/plotGraph', methods=['GET'])
@login_required
def plot_graph():
    workout_counts_list = [count for (count,) in Workout.query.with_entities(Workout.count).filter_by(author=current_user).all()]
    workout_dates_list = [date for (date,) in Workout.query.with_entities(Workout.date_posted).filter_by(author=current_user).all()]

    if not workout_counts_list or not workout_dates_list:
        flash("No workouts available to plot.")
        return redirect(url_for('main.get_workouts'))

    fig, ax = plt.subplots()
    ax.plot(workout_dates_list, workout_counts_list, marker='o')
    ax.set_xlabel('Date of Workout', labelpad=20)
    ax.set_ylabel('Workout Count', labelpad=20)
    fig.autofmt_xdate()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)

    return send_file(buf, mimetype='image/png', as_attachment=False, download_name='workout_plot.png')

@main.route('/api/updateWorkout/<int:workout_id>', methods=['GET','POST', 'PUT'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    if request.method == 'POST':
        workout.count = request.form.get('count')
        workout.comment = request.form.get('comment')

        db.session.commit()
        flash("Your workout has been updated")
        return redirect(url_for('main.get_workouts'))

    return render_template("update_workout.html", workout=workout)

@main.route('/api/deleteWorkout/<int:workout_id>', methods=['GET'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    db.session.delete(workout)
    db.session.commit()

    flash("Your workout has been deleted")
    return redirect(url_for('main.get_workouts'))