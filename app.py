from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bikes.db'
db = SQLAlchemy(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Try again.')
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_bikes = Bike.query.count()
    available_bikes = Bike.query.filter_by(is_available=True).count()
    rented_bikes = Bike.query.filter_by(is_available=False).count()
    pending_bookings = Booking.query.filter_by(status='pending').count()
    recent_bookings = Booking.query.filter(Booking.status != 'rejected').order_by(Booking.id.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
        total_bikes=total_bikes,
        available_bikes=available_bikes,
        rented_bikes=rented_bikes,
        pending_bookings=pending_bookings,
        recent_bookings=recent_bookings
    )

@app.route('/admin/rejected')
@login_required
def rejected_log():
    rejected_bookings = Booking.query.filter_by(status='rejected').order_by(Booking.id.desc()).all()
    return render_template('admin/rejected.html', rejected_bookings=rejected_bookings)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/booking/<int:booking_id>/approve')
@login_required
def approve_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'approved'
    db.session.commit()
    flash('Booking approved.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/<int:booking_id>/reject')
@login_required
def reject_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'rejected'
    db.session.commit()
    flash('Booking rejected.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/<int:booking_id>/delete')
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/<int:booking_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if request.method == 'POST':
        booking.customer_name = request.form['customer_name']
        booking.customer_phone = request.form['customer_phone']
        booking.booking_date = datetime.strptime(request.form['booking_date'], '%Y-%m-%d')
        booking.status = request.form['status']
        db.session.commit()
        flash('Booking updated.')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit_booking.html', booking=booking)

@app.route('/')
def index():
    all_bikes = Bike.query.all()
    return render_template('index.html', bikes=all_bikes)

class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    engine_cc = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    image_file = db.Column(db.String(100), default='default_bike.jpg')

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(15), nullable=False)
    time_out = db.Column(db.DateTime, nullable=False)
    time_returned = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(15), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    bike = db.relationship('Bike', backref='bookings')

with app.app_context():
    db.create_all()


@app.route('/bikes')
def bikes():
    all_bikes = Bike.query.all()
    return render_template('bikes.html', bikes=all_bikes)


@app.route('/bikes/<int:bike_id>')
def bike_detail(bike_id):
    bike = Bike.query.get_or_404(bike_id)
    return render_template('bike_detail.html', bike=bike)

@app.route('/book/<int:bike_id>', methods=['GET', 'POST'])
def booking(bike_id):
    bike = Bike.query.get_or_404(bike_id)
    if request.method == 'POST':
        new_booking = Booking(
            bike_id=bike.id,
            customer_name=request.form['customer_name'],
            customer_phone=request.form['customer_phone'],
            booking_date=datetime.strptime(request.form['booking_date'], '%Y-%m-%d'),
            status='pending'
        )
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('confirmation'))
    return render_template('booking.html', bike=bike)
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/admin/history')
@login_required
def history_log():
    query = Booking.query

    customer = request.args.get('customer')
    bike_id = request.args.get('bike_id')
    date = request.args.get('date')

    if customer:
        query = query.filter(Booking.customer_name.ilike(f'%{customer}%'))
    if bike_id:
        query = query.filter(Booking.bike_id == bike_id)
    if date:
        query = query.filter(db.func.date(Booking.booking_date) == date)

    all_bookings = query.order_by(Booking.id.desc()).all()
    all_bikes = Bike.query.all()

    return render_template('admin/history.html', bookings=all_bookings, bikes=all_bikes)

if __name__ == '__main__':
    app.run(debug=True)