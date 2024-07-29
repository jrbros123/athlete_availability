from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' 


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///athletes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Athlete model
class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    availability_date = db.Column(db.Date, nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database and table(s)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Welcome to the Athlete Availability App!"

@app.route('/update_availability', methods=['GET', 'POST'])
def update_availability():
    if request.method == 'POST':
        email = request.form['email']
        availability_date = request.form['availability_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        try:
            # Check if the athlete already exists
            athlete = Athlete.query.filter_by(email=email).first()
            if athlete:
                # Update existing athlete
                athlete.availability_date = datetime.strptime(availability_date, '%Y-%m-%d').date()
                athlete.start_time = datetime.strptime(start_time, '%H:%M').time()
                athlete.end_time = datetime.strptime(end_time, '%H:%M').time()
                athlete.last_update = datetime.utcnow()
            else:
                # Create new athlete entry
                athlete = Athlete(
                    email=email,
                    availability_date=datetime.strptime(availability_date, '%Y-%m-%d').date(),
                    start_time=datetime.strptime(start_time, '%H:%M').time(),
                    end_time=datetime.strptime(end_time, '%H:%M').time()
                )
                db.session.add(athlete)
            
            db.session.commit()
            flash('Availability updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')

        return redirect(url_for('update_availability'))

    return render_template('update_availability.html')

if __name__ == '__main__':
    app.run(debug=True)
