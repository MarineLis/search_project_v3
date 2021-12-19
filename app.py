from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

from Forms.ContestForm import ContestForm
from Forms.ContestFormEdit import ContestFormEdit
from Forms.FestForm import FestForm
from Forms.FestFormEdit import FestFormEdit
from Forms.LoginForm import LoginForm
from Forms.PeopleFormEdit import PeopleFormEdit
from Forms.PlaceForm import PlaceForm
from Forms.PlaceFormEdit import PlaceFormEdit
from Forms.RegistrationFrom import RegistrationForm
from Forms.SearchForm import SearchForm
from Forms.UserForm import UserForm
import os

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gimwfhephkloso:b81611ec8a96c8cd82f2c4bd4a5fb5cd0dc8da7e95089535113297926969ffdb@ec2-63-33-239-176.eu-west-1.compute.amazonaws.com:5432/dajtegge93na72'
# else:
#     app.debug = False
#     app.config['SECRET_KEY'] = 'laba3marina'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vhvdhatwvgwrqi:017ae15421526ef1936ecac9a042672ff9f4e3107cec577d871e8620bfeb94f1@ec2-54-163-254-204.compute-1.amazonaws.com:5432/d5bk6gtqhqg32k'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contest(db.Model):
    tablename = 'contest'
    contest_name = db.Column(db.String(300), primary_key=True)
    fest_name = db.Column(db.String(20), db.ForeignKey('fest.fest_name'))


class People(db.Model):
    tablename = 'People'
    people_email = db.Column(db.String(20), primary_key=True)
    people_name = db.Column(db.String(20))
    people_phone = db.Column(db.String(20))
    people_birthday = db.Column(db.Date)
    people_password = db.Column(db.String(20))

    people_fest = db.relationship('Fest')


class association(db.Model):
    __tablename__ = 'associate_table'
    left_name = db.Column(db.String(20), db.ForeignKey('fest.fest_name'), primary_key=True)
    right_name = db.Column(db.String(20), db.ForeignKey('place.place_name'), primary_key=True)


class Fest(db.Model):
    __tablename__ = 'fest'
    fest_name = db.Column(db.String(20), primary_key=True)
    people_email = db.Column(db.String(20), db.ForeignKey('people.people_email'))
    fest_date = db.Column(db.Date)

    place_name_fk = db.relationship("Place", secondary='associate_table')
    fest_contest = db.relationship('Contest')


class CityHasPlace(db.Model):
    __tablename__ = 'city_has_place'
    place_name = db.Column(db.String(20), db.ForeignKey('place.place_name'), primary_key=True)
    city_name = db.Column(db.String(20), db.ForeignKey('city.city_name'), primary_key=True)


class Place(db.Model):
    __tablename__ = 'place'
    place_name = db.Column(db.String(20), primary_key=True)
    place_adress = db.Column(db.String(100))
    place_price = db.Column(db.Integer)

    fest_name_fk = db.relationship("Fest", secondary='associate_table')

    city_name_fk = db.relationship("City", secondary='city_has_place')


class City(db.Model):
    __tablename__ = 'city'
    city_name = db.Column(db.String(20), primary_key=True)
    city_population = db.Column(db.Integer)
    city_balance = db.Column(db.Integer)

    place_name_fk = db.relationship('Place', secondary='city_has_place')


# создание всех таблиц
db.create_all()

#очистка всех таблиц
db.session.query(CityHasPlace).delete()
db.session.query(City).delete()
db.session.query(association).delete()
db.session.query(Contest).delete()
db.session.query(Fest).delete()
db.session.query(People).delete()
db.session.query(Place).delete()


#создане объектов
Kyiv = City(city_name='Kyiv',
                  city_balance=1000,
                  city_population=3000000
                  )

Odessa = City(city_name='Odessa',
                  city_balance=200,
                  city_population=80000
                  )

Zhitomyr = City(city_name='Zhitomyr',
                 city_balance=30000,
                 city_population=50000000
                 )

Carpathians = City(city_name='Carpathians',
                  city_balance=40000,
                  city_population=70000000
                  )

Kharkov = City(city_name='Kharkov',
                   city_balance=50000,
                   city_population=30000000
                   )

# insert into People (people_email, people_name, people_phone, people_birthday) values ('aaa@gmail.com', 'aaa', '+47447474774', '1835-1-23');
# insert into People (people_email, people_name, people_phone, people_birthday) values ('bbb@gmail.com', 'bbb', '+399489384334', '487-2-21');
# insert into People (people_email, people_name, people_phone, people_birthday) values ('ccc@gmail.com', 'ccc', '+23232332323', '1637-6-23');
# insert into People (people_email, people_name, people_phone, people_birthday) values ('ddd@gmail.com', 'ddd', '+39842349238492', '1-1-1');
# insert into People (people_email, people_name, people_phone, people_birthday) values ('eee@gmail.com', 'eee', '+304930432432', '1049-1-1');

aaa = People(people_email='aaa@gmail.com',
             people_name='aaa',
             people_phone='+47447474774',
             people_birthday="1995-01-23",
             people_password='aaa123'
             )

bbb = People(people_email='bbb@gmail.com',
             people_name='bbb',
             people_phone='+399489384334',
             people_birthday='1987-2-21',
             people_password='bbb123'
             )

ccc = People(people_email='ccc@gmail.com',
             people_name='ccc',
             people_phone='+23232332323',
             people_birthday='1967-6-23',
             people_password='ccc123'
             )

ddd = People(people_email='ddd@gmail.com',
             people_name='ddd',
             people_phone='+39842349238492',
             people_birthday='2001-1-1',
             people_password='ddd123'
             )

eee = People(people_email='eee@gmail.com',
             people_name='eee',
             people_phone='+304930432432',
             people_birthday='1998-1-1',
             people_password='eee123'
             )

admin = People(people_email='admin@gmail.com',
               people_name='Marinka',
               people_phone='+380660336265',
               people_birthday='2000-10-17',
               people_password='admin')

# insert into Fest (fest_name, people_email, fest_date) values ('food_fest', 'ddd@gmail.com', '1051-1-4');
# insert into Fest (fest_name, people_email, fest_date) values ('musical_fest', 'bbb@gmail.com', '1619-3-8');
# insert into Fest (fest_name, people_email, fest_date) values ('math_fest', 'aaa@gmail.com', '1994-12-2');
# insert into Fest (fest_name, people_email, fest_date) values ('animal_fest', 'ddd@gmail.com', '538-10-29');
# insert into Fest (fest_name, people_email, fest_date) values ('football_fest', 'ddd@gmail.com', '1-1-1');

food_fest = Fest(fest_name='food_fest',
           people_email='ddd@gmail.com',
           fest_date='2021-1-4')

musical_fest = Fest(fest_name='musical_fest',
                  people_email='bbb@gmail.com',
                  fest_date='2021-3-8'
                  )

math_fest = Fest(fest_name='math_fest',
                 people_email='aaa@gmail.com',
                 fest_date='2021-12-2'
                 )

animal_fest = Fest(fest_name='animal_fest',
                    people_email='ddd@gmail.com',
                    fest_date='2021-10-29'
                    )

football_fest = Fest(fest_name='football_fest',
                 people_email='ddd@gmail.com',
                 fest_date='2021-1-1'
                 )

# insert into Place (place_name, place_adress) values ('museum', 'Киевская, Киев, Ковальський провулок, 5, 5-26');
# insert into Place (place_name, place_adress) values ('club', 'Hindenburgstraße 7a, 57072 Siegen');
# insert into Place (place_name, place_adress) values ('restaurant', 'Hindenburgstraße 12, 57072 Siegen');
# insert into Place (place_name, place_adress) values ('stadion', 'Leimbachstadion, Leimbachstraße 263, 57074 Siegen');
# insert into Place (place_name, place_adress) values ('theatre', 'Morleystraße 1, 57072 Siegen');

museum = Place(place_name='museum',
               place_adress='Киевская, Киев, Ковальський провулок, 5, 5-26',
               place_price=100
               )

club = Place(place_name='club',
             place_adress='Пушкинская 7a, 57072',
             place_price=300
             )

restaurant = Place(place_name='restaurant',
                   place_adress='Лермонтовская 12, 57072 Siegen',
                   place_price=600
                   )

stadion = Place(place_name='stadion',
                place_adress='Ахматовская 263, 57074 Siegen',
                place_price=500
                )

theatre = Place(place_name='theatre',
                place_adress='Мюнхаузеновская 1, 57072 Siegen',
                place_price=200
                )

# insert into Contest (contest_name, fest_name) values ('ball', 'football_fest');
# insert into Contest (contest_name, fest_name) values ('present', 'math_fest');
# insert into Contest (contest_name, fest_name) values ('music', 'musical_fest');
# insert into Contest (contest_name, fest_name) values ('bottle of wine', 'musical_fest');
# insert into Contest (contest_name, fest_name) values ('animal', 'animal_fest');

ball = Contest(contest_name='FOOTBALLFEST is the ultimate 3 day adult football tour (6 a-side) for Male and Female teams. Hosted in Bournemouth, you can enjoy the award winning beaches, vibrant nightlife, play football and have a good time! All at an affordable price',
               fest_name='football_fest'
               )

present = Contest(contest_name='The Call for Proposals at MAA MathFest 2022 is coming soon! Please keep checking here for the latest updates, as the submission portal will launch in the coming few weeks. In the meantime, please email meetings@maa.org with any questions.',
                  fest_name='math_fest'
                  )

music = Contest(contest_name='The worlds best music festivals span Glastonbury, Tomorrowland, Coachella, Primavera Sound, UMF and many more, across the continents of Europe, North America, South America, Africa and Asia.',
                fest_name='musical_fest'
                )


animal = Contest(contest_name='ANIMAL FEST is a two-day event addressed to lovers of all companion animals, it is a real paradise for enthusiasts of dogs, cats, aquarium and terrariums, exotic birds and smaller animals',
                   fest_name='animal_fest'
                   )

ddd.people_fest.append(food_fest)
bbb.people_fest.append(musical_fest)
aaa.people_fest.append(math_fest)
ddd.people_fest.append(animal_fest)
ddd.people_fest.append(football_fest)

football_fest.fest_contest.append(ball)
math_fest.fest_contest.append(present)
musical_fest.fest_contest.append(music)
#musical_fest.fest_contest.append(bottle_of_wine)
animal_fest.fest_contest.append(animal)

food_fest.place_name_fk.append(museum)
musical_fest.place_name_fk.append(club)
math_fest.place_name_fk.append(restaurant)
animal_fest.place_name_fk.append(stadion)
football_fest.place_name_fk.append(theatre)

museum.city_name_fk.append(Kyiv)
club.city_name_fk.append(Zhitomyr)
restaurant.city_name_fk.append(Kharkov)
stadion.city_name_fk.append(Carpathians)
theatre.city_name_fk.append(Odessa)

db.session.add_all([aaa, bbb, ccc, ddd, eee,admin,
                    food_fest, musical_fest, math_fest, animal_fest, football_fest,
                    Kyiv, Odessa,Zhitomyr, Carpathians, Kharkov,
                    museum, club, restaurant, stadion, theatre,
                    ball, present, music,
                    #bottle_of_wine,
                    animal

                    ])

db.session.commit()


def dropSession():
    session['people_email'] = ''
    session['role'] = 'unlogged'


def newSession(email, pw):
    session['people_email'] = email
    if pw == 'admin':
        session['role'] = 'admin'
    else:
        session['role'] = 'people_email'

@app.route('/')
def root():
    try:
        if not session['people_email']:
            return redirect('/login')
    except:
        session['people_email'] = ''
        session['role'] = 'unlogged'
        return redirect('/login')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate():
            try:
                res = db.session.query(People).filter(People.people_email == form.people_email.data).one()
            except:
                form.people_email.errors = ['people doesnt exist']
                return render_template('login.html', form=form)
            if res.people_password == form.people_password.data:
                newSession(res.people_email, res.people_password)
                return redirect('/')
            else:
                form.people_password.errors = ['wrong password']
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    dropSession()
    return redirect('/login')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate():
            try:
                new_people = People(
                    people_email=form.people_email.data,
                    people_password=form.people_confirm_password.data
                )
                db.session.add(new_people)
                db.session.commit()
                newSession(new_people.people_email, new_people.people_password)
                return render_template('success.html')
            except:
                form.people_email.errors = ['this user is registered']
                return render_template('registration.html', form=form)
        else:
            return render_template('registration.html', form=form)

    return render_template('registration.html', form=form)


@app.route('/infouser', methods=['GET', 'POST'])
def user_info():
    result = db.session.query(People).all()
    return render_template('infouser.html', result=result)

@app.route('/edit_user/<string:email>', methods=['GET', 'POST'])
def edit_user(email):
    form = PeopleFormEdit()
    result = db.session.query(People).filter(People.people_email == email).one()

    if request.method == 'GET':

        form.people_name.data = result.people_name
        form.people_email.data = result.people_email
        form.people_birthday.data = result.people_birthday
        form.people_phone.data = result.people_phone

        return render_template('edit_user.html', form=form, form_name=email)
    elif request.method == 'POST':
        if form.validate() and form.validate_birthday():
            result.people_name = form.people_name.data
            result.user_email = form.people_email.data
            result.people_birthday = form.people_birthday.data.strftime("%Y-%m-%d")
            result.people_phone = form.people_phone.data

            db.session.commit()
            return redirect('/infouser')
        else:
            if not form.validate_birthday():
                form.people_birthday.errors = ['should be >1900']
            return render_template('edit_user.html', form=form)


@app.route('/people')
def users():
    if session['role'] == 'admin':
        result = db.session.query(People).all()
        return render_template('all_people.html', result=result)
    else:
        return redirect('/login')


@app.route('/people/<string:email>')
def poeple_info(email):
    if session['role'] != 'unlogged':
        res = db.session.query(People).filter(People.people_email == email).one()
        return render_template('people_info.html', people=res)
    else:
        return redirect('/login')




@app.route('/edit_people/<string:email>', methods=['GET', 'POST'])
def edit_people(email):
    form = PeopleFormEdit()
    result = db.session.query(People).filter(People.people_email == email).one()

    if request.method == 'GET':

        form.people_name.data = result.people_name
        form.people_email.data = result.people_email
        form.people_birthday.data = result.people_birthday
        form.people_phone.data = result.people_phone

        return render_template('edit_people.html', form=form, form_name=email)
    elif request.method == 'POST':
        if form.validate() and form.validate_birthday():
            result.people_name = form.people_name.data
            result.user_email = form.people_email.data
            result.people_birthday = form.people_birthday.data.strftime("%Y-%m-%d")
            result.people_phone = form.people_phone.data

            db.session.commit()
            return redirect('/people')
        else:
            if not form.validate_birthday():
                form.people_birthday.errors = ['should be >1900']
            return render_template('edit_people.html', form=form)


@app.route('/edit_fest/<string:name>', methods=['GET', 'POST'])
def edit_fest(name):
    form = FestFormEdit()
    result = db.session.query(Fest).filter(Fest.fest_name == name).one()

    if request.method == 'GET':

        form.fest_name.data = result.fest_name
        form.fest_date.data = result.fest_date

        return render_template('edit_fest.html', form=form, form_name=name)

    elif request.method == 'POST':
        if form.validate() and form.validate_date():

            result.fest_name = form.fest_name.data
            result.fest_date = form.fest_date.data.strftime("%Y-%m-%d")

            db.session.commit()
            return redirect('/fest')
        else:
            if not form.validate_date():
                form.fest_date.errors = ['should be > 2020']
            return render_template('edit_fest.html', form=form)


@app.route('/edit_contest/<string:name>', methods=['GET', 'POST'])
def edit_contest(name):
    form = ContestFormEdit()
    result = db.session.query(Contest).filter(Contest.contest_name == name).one()

    if request.method == 'GET':

        form.contest_name.data = result.contest_name

        return render_template('edit_contest.html', form=form, form_name='Edit Contest')
    elif request.method == 'POST':

        result.contest_name = form.contest_name.data

        db.session.commit()
        return redirect('/contest')


@app.route('/edit_place/<string:name>', methods=['GET', 'POST'])
def edit_place(name):
    form = PlaceFormEdit()
    result = db.session.query(Place).filter(Place.place_name == name).one()

    if request.method == 'GET':

        form.place_name.data = result.place_name
        form.place_adress.data = result.place_adress
        form.place_price.data = result.place_price

        return render_template('edit_place.html', form=form, form_name='Edit Place')

    try:
        result = db.session.query(Place).filter(Place.place_name == form.place_name.data).one()
        if result != 0:
            return render_template('edit_place.html', place_name="Place exist", form=form)
    except:
        pass

    if request.method == 'POST':

        if form.validate() and form.check_price():
            result.place_name = form.place_name.data
            result.place_adress = form.place_adress.data
            result.place_price = form.place_price.data

            db.session.commit()
            return redirect('/place')
        else:
            if not form.check_price():
                form.place_price.errors = ['should be >0']
            return render_template('edit_place.html', form=form)


@app.route('/create_people', methods=['POST', 'GET'])
def create_people():
    form = UserForm()
    try:
        result = db.session.query(People).filter(People.people_name == form.people_name.data).one()
        if result != 0:
            return render_template('create_people.html', people_name="People exist", form=form)
    except:
        pass

    if request.method == 'POST':
        if form.validate() and form.validate_birthday():
            new_people = People(
                people_name=form.people_name.data,
                people_birthday=form.people_birthday.data.strftime("%Y-%m-%d"),
                people_email=form.people_email.data,
                people_phone=form.people_phone.data,
            )
            db.session.add(new_people)
            db.session.commit()
            return redirect('/people')
        else:
            if not form.validate_birthday():
                form.people_birthday.errors = ['should be >1900']
            return render_template('create_people.html', form=form)
    elif request.method == 'GET':
        return render_template('create_people.html', form=form)


@app.route('/delete_people/<string:email>', methods=['GET', 'POST'])
def delete_people(email):
    result = db.session.query(People).filter(People.people_email == email).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/people')


@app.route('/create_contest', methods=['POST', 'GET'])
def create_contest():
    form = ContestForm()
    try:
        result = db.session.query(Contest).filter(Contest.contest_name == form.contest_name.data).one()
        if result != 0:
            return render_template('create_contest.html', contest_name="Contest exist", form=form)
    except:
        pass
    if request.method == 'POST':
        new_contest = Contest(
            contest_name=form.contest_name.data,
        )
        db.session.add(new_contest)
        db.session.commit()
        return redirect('/contest')
    elif request.method == 'GET':
        return render_template('create_contest.html', form=form)


@app.route('/delete_contest/<string:name>', methods=['GET', 'POST'])
def delete_contest(name):
    result = db.session.query(Contest).filter(Contest.contest_name == name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/contest')


@app.route('/create_fest', methods=['POST', 'GET'])
def create_fest():
    form = FestForm()
    try:
        result = db.session.query(Fest).filter(Fest.fest_name == form.fest_name.data).one()
        if result != 0:
            return render_template('create_fest.html', fest_name="Fest exist", form=form)
    except:
        pass
    if request.method == 'POST':
        if form.validate() and form.validate_date():
            new_fest = Fest(
                fest_name=form.fest_name.data,
                fest_date=form.fest_date.data.strftime("%Y-%m-%d"),
                people_email=form.people_email.data
            )
            db.session.add(new_fest)
            db.session.commit()
            return redirect('/fest')
        else:
            if not form.validate_date():
                form.fest_date.errors = ['should be > 2020']
            return render_template('create_fest.html', form=form)
    elif request.method == 'GET':
        return render_template('create_fest.html', form=form)


@app.route('/delete_fest/<string:name>', methods=['GET', 'POST'])
def delete_fest(name):
    result = db.session.query(Fest).filter(Fest.fest_name == name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/fest')


@app.route('/create_place', methods=['POST', 'GET'])
def create_place():
    form = PlaceForm()
    try:
        result = db.session.query(Place).filter(Place.place_name == form.place_name.data).one()
        if result != 0:
            return render_template('create_place.html', place_name="Place exist", form=form)
    except:
        pass
    if request.method == 'POST':
        if form.validate() and form.check_price():
            new_place = Place(
                place_name=form.place_name.data,
                place_adress=form.place_adress.data,
                place_price=form.place_price.data
            )
            db.session.add(new_place)
            db.session.commit()
            return redirect('/place')
        else:
            if not form.check_price():
                form.place_price.errors = ['should be >0']
            return render_template('create_place.html', form=form)
    elif request.method == 'GET':
        return render_template('create_place.html', form=form)


@app.route('/delete_place/<string:name>', methods=['GET', 'POST'])
def delete_place(name):
    result = db.session.query(Place).filter(Place.place_name == name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/place')


@app.route('/contest', methods=['GET'])
def all_contest():
    result = db.session.query(Contest).all()

    return render_template('all_contest.html', result=result)


@app.route('/fest', methods=['GET'])
def all_fest():
    result = db.session.query(Fest).all()

    return render_template('all_fest.html', result=result)


@app.route('/place', methods=['GET'])
def all_place():
    result = db.session.query(Place).all()

    return render_template('all_place.html', result=result)


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()

    if request.method == 'POST':
        if form.type_field.data == 'fest_name':
            res = db.session.query(Fest).filter(Fest.fest_name == form.search_value.data).all()
        elif form.type_field.data == 'fest_date':
            res = db.session.query(Fest).filter(Fest.fest_date == form.search_value.data).all()

        return render_template('search_result.html', vacancies=res)
    else:
        return render_template('search.html', form=form)


if __name__ == "__main__":
    # app.debug = True
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
