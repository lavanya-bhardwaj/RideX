from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bikes.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

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
if __name__ == '__main__':
    app.run(debug=True)