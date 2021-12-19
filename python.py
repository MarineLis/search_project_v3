if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:180801pg@localhost/postgres'#'postgres://postgres:postgres@localhost:5432/postgresdb'

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
