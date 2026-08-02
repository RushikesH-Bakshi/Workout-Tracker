from flask import Blueprint, flash, render_template, url_for, request, redirect, send_file, jsonify
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
def profile():
    if not current_user.is_authenticated:
        return jsonify({"message": "Not authenticated"}), 401

    return jsonify({"user": {"id": current_user.id, "name": current_user.name, "email": current_user.email}}), 200

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
    
@main.route('/api/workouts', methods=['GET', 'POST'])
@login_required
def workouts_collection():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        pagination = Workout.query.filter_by(author=current_user).order_by(Workout.id.desc()).paginate(page=page, per_page=6, error_out=False)
        workouts = [{"id": workout.id, "count": workout.count, "comment": workout.comment, "date_posted": workout.date_posted.isoformat()} for workout in pagination.items]
        return jsonify({"workouts": workouts, "page": pagination.page, "pages": pagination.pages, "has_next": pagination.has_next}), 200

    data = request.get_json(silent=True) or request.form
    count = data.get('count')
    comment = data.get('comment')

    if count is None or comment is None:
        return jsonify({"message": "Count and comment are required"}), 400

    workout = Workout(count=int(count), comment=comment, author=current_user)
    db.session.add(workout)
    db.session.commit()

    return jsonify({"message": "Workout created successfully", "workout": {"id": workout.id, "count": workout.count, "comment": workout.comment, "date_posted": workout.date_posted.isoformat()}}), 201


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

@main.route('/api/workouts/<int:workout_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def workout_detail(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    if workout.author != current_user:
        return jsonify({"message": "Forbidden"}), 403

    if request.method == 'GET':
        return jsonify({"workout": {"id": workout.id, "count": workout.count, "comment": workout.comment, "date_posted": workout.date_posted.isoformat()}}), 200

    if request.method == 'PUT':
        data = request.get_json(silent=True) or request.form
        count = data.get('count')
        comment = data.get('comment')

        if count is not None:
            workout.count = int(count)
        if comment is not None:
            workout.comment = comment

        db.session.commit()
        return jsonify({"message": "Workout updated successfully", "workout": {"id": workout.id, "count": workout.count, "comment": workout.comment, "date_posted": workout.date_posted.isoformat()}}), 200

    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully"}), 200


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