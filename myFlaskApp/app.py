from flask import Flask, render_template, flash, redirect, url_for, session, request, logging #call templates
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt  #to encrypt Password



app = Flask(__name__)

# Config Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize MYSQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/TS')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=1,max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email',[validators.Length(min=6,max=50)])
    password = StringField('Password',[
            validators.DataRequired(),
            validators.EqualTo('confirm'),
            validators.EqualTo('confirm', message='Passwords do not match')

    ])
    confirm = PasswordField('Confirm password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))


        # Create cursor
        cur = mysql.connection.cursor()


        cur.execute("INSERT INTO user(name,  email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return render_template('register.html')
    return render_template('register.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)
