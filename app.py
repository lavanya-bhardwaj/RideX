from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from functools import wraps


app = Flask(__name__)
app.secret_key = 'cbr_admin_secret_2026'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'cbr2026'
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
    recent_bookings = Booking.query.order_by(Booking.id.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
        total_bikes=total_bikes,
        available_bikes=available_bikes,
        rented_bikes=rented_bikes,
        pending_bookings=pending_bookings,
        recent_bookings=recent_bookings
    )

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

@app.route('/seed')
def seed():
    bikes = [
        Bike(name='Royal Enfield Classic 350', engine_cc=350, price_per_day=1500.0, is_available=True),
        Bike(name='Royal Enfield Himalayan', engine_cc=411, price_per_day=2000.0, is_available=True),
        Bike(name='Bajaj Pulsar NS200', engine_cc=200, price_per_day=1200.0, is_available=True),
        Bike(name='TVS Apache RTR 160', engine_cc=160, price_per_day=1000.0, is_available=True)
    ]
    db.session.add_all(bikes)
    db.session.commit()
    return 'Bikes added!'

@app.route('/check')
def check():
    all_bikes = Bike.query.all()
    return str([(b.id, b.name) for b in all_bikes])

@app.route('/bikes')
def bikes():
    all_bikes = Bike.query.all()
    return render_template('bikes.html', bikes=all_bikes)

@app.route('/reseed')
def reseed():
    Bike.query.delete()
    bikes = [
        Bike(name='Royal Enfield Classic 350', engine_cc=350, price_per_day=1500, is_available=True, image_file='royal_enfield_classic_350.jpg'),
        Bike(name='Royal Enfield Himalayan', engine_cc=411, price_per_day=2000, is_available=True, image_file='royal_enfield_himalayan.jpg'),
        Bike(name='Bajaj Pulsar NS200', engine_cc=200, price_per_day=1000, is_available=True, image_file='bajaj_pulsar_ns200.jpg'),
        Bike(name='Yamaha MT-15', engine_cc=155, price_per_day=1200, is_available=True, image_file='yamaha_mt-15.jpg'),
        Bike(name='TVS Apache RTR 160', engine_cc=160, price_per_day=900, is_available=True, image_file='tvs_apache_rtr_160.jpg'),
    ]
    db.session.add_all(bikes)
    db.session.commit()
    return 'Done!'

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

if __name__ == '__main__':
    app.run(debug=True)