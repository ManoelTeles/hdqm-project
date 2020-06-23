from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    host = TextField('Host:', validators=[validators.required()])
    database = TextField('Database:', validators=[validators.required()])
    user = TextField('User:', validators=[validators.required()])
    password = TextField('Password:', validators=[validators.required()])
    database_conn = TextField('Password:', validators=[validators.required()])

    @app.route("/", methods=['GET', 'POST'])
    def main():
        return render_template('home.html')

    @app.route("/driver", methods=['GET', 'POST'])
    def dbDriver():
        form = ReusableForm(request.form)

        if request.method == 'POST':
            host=request.form['host']
            database=request.form['database']
            user=request.form['user']
            password=request.form['password']
            database_conn=request.form['database_conn']
            print( host, database, user, password, database_conn)

        if form.validate():
        # Save the comment here.
            flash('Thanks for registration ' + host)
        else:
            flash('Error: All the form fields are required. ')
    
        return render_template('dbDriver.html', form=form)

if __name__ == "__main__":
    app.run()