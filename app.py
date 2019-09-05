import random, string
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists

##########################DATABASE##################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:TestPassword@localhost/Doctor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class Doctors(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    time = db.Column(db.String(64), index=True)
    kind = db.Column(db.String(256), index=True)


@app.route('/')
def index():
    return "Doctors Site!!!"


@app.route('/insert-dummy-data')
def InsertDummyData():
    for i in range(100):
        data_obj = Doctors(
            name = randomString(5) + randomString(4),
            time = str(random.randint(1,10)) + ':00 AM',
            kind = randomString(6) + randomString(6)
        )
        db.session.add(data_obj)
        db.session.commit()
    return "Done!!!!"


@app.route('/get-list')
def GetDoctorsList():
    result_list = []
    doctors_obj = Doctors.query.all()
    for i in doctors_obj:
        result_list.append(i.name)
    new_dict = {}
    new_dict['Doctor Names'] = result_list
    return new_dict


@app.route('/list-appointments/<name>/<time>')
def ListAppointments(name, time):
    result_list = []
    doctors_obj = Doctors.query.filter_by(name=name, time=time)
    for i in doctors_obj:
        result_list.append(i.kind)
    new_dict = {}
    new_dict['Appointment List'] = result_list
    return new_dict


@app.route('/delete-appointments/<name>/<time>')
def DeleteAppointments(name, time):
    Doctors.query.filter_by(name=name, time=time).delete()
    db.session.commit()
    new_dict = {}
    new_dict['message'] = f'Appointment for {name} is deleted successfully!!!'
    return new_dict



if __name__ == '__main__':
    app.run(debug=True)
