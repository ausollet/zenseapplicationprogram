import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    check = db.Column(db.Integer)
    log = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.username

class RegisterForm(FlaskForm):
    username = StringField('username: ', validators=[DataRequired()])
    email = StringField('email id: ', validators=[DataRequired()])
    password = PasswordField('password:',validators=[DataRequired()])
    confirm_password = PasswordField('confirm password: ',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Submit')
    
    app.config.update(
        DEBUG = True,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 465,
        MAIL_USE_SSL = True,
        MAIL_USERNAME = 'vzmpserver@gmail.com',
        MAIL_PASSWORD = 'topsecret'
        )

mail = Mail(app)


class LoginForm(FlaskForm):
    username = StringField('username:', validators=[DataRequired()])
    password = PasswordField('password:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/Register', methods=['GET', 'POST'])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        useremail = User.query.filter_by(email=form.email.data).first()
        if (user is None) and (useremail is None):
            user = User(username=form.username.data,password=generate_password_hash(form.password.data),email=form.email.data,address=form.address.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            msg = Message("Sent verification link", sender="vksserverpython@gmail.com", recipients=[user.email])
            link = url_for('UserConfirmation', username=user.username)
            msg.body = "click here to confirm {}".format(link)
            mail.send(msg)

            return redirect(url_for('Confirmation'))
        else:
            session['known']=True
            flash('username or email already exists!')
            return redirect(url_for('Register'))
        session['username'] = form.username.data
        session['password'] = form.password.data
        return redirect(url_for('Register'))
    return render_template('Register.html', form = form, username = session.get('username'),password = session.get('password'),known = session.get('known'))

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('incorrect username/password!')
            return redirect(url_for('Login'))
        else:
            if check_password_hash(user.password, form.password.data) and user.check == 1:
                user.log = 1
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index', username=user.username))
            elif not user.check == 1:
                flash('please confirm your email, then you can login')
            else:
                flash('incorrect username/password!')
            return redirect(url_for('Login'))
        session['username'] = form.username.data
        session['password'] = form.password.data
        return redirect(url_for('Login'))
    return render_template('Login.html', form = form, username = session.get('username'),password = session.get('password'))

@app.route('/Lost', methods=['GET', 'POST'])
def score():
    return render_template('score.html') 

@app.route('/index/<username>', methods=['GET', 'POST'])
def index(username):
    import random
    rc = 7
    mines = 16
    grid = []
    for j in range(rc):
        minigrid = []
        for k in range(rc):
            minigrid.append(0)
        grid.append(minigrid[:])
    i = 0
    while(i<mines):
        x = random.randint(0, rc-1)
        y = random.randint(0, rc-1)
        if(not grid[x][y] == '*'):
            grid[x][y] = '*'
            i+=1
    
    for j in range(rc):
        for k in range(rc):
            if(j>0):
                if(grid[j-1][k]=='*' and not(grid[j][k]=='*')):
                    grid[j][k]+=1
                if(k<rc-1):
                    if(grid[j-1][k+1]=='*' and not(grid[j][k]=='*')):
                        grid[j][k]+=1
                if(k>0):
                    if(grid[j-1][k-1]=='*' and not(grid[j][k]=='*')):
                        grid[j][k]+=1
            if(j<rc-1):
                if(grid[j+1][k]=='*' and not(grid[j][k]=='*')):
                    grid[j][k]+=1
                if(k<rc-1):
                    if(grid[j+1][k+1]=='*' and not(grid[j][k]=='*')):
                        grid[j][k]+=1
                if(k>0):
                    if(grid[j+1][k-1]=='*' and not(grid[j][k]=='*')):
                        grid[j][k]+=1
            if(k<rc-1):
                if(grid[j][k+1]=='*' and not(grid[j][k]=='*')):
                    grid[j][k]+=1
            if(k>0):
                if(grid[j][k-1]=='*' and not(grid[j][k]=='*')):
                    grid[j][k]+=1

    print(grid)
    user=User.query.filter_by(username=username).first()
    if(user.log == 1):
        return render_template('index.html',url = url_for('score'), username = username, g1 = grid[0][0], g2 = grid[0][1], g3 = grid[0][2], g4 = grid[0][3], g5 = grid[0][4], g6 = grid[0][5], g7 = grid[0][6], g8 = grid[1][0], g9 = grid[1][1], g10 = grid[1][2], g11 = grid[1][3], g12 = grid[1][4], g13 = grid[1][5], g14 = grid[1][6], g15 = grid[2][0], g16 = grid[2][1], g17 = grid[2][2], g18 = grid[2][3], g19 = grid[2][4], g20 = grid[2][5], g21 = grid[2][6], g22 = grid[3][0], g23 = grid[3][1], g24 = grid[3][2], g25 = grid[3][3], g26 = grid[3][4], g27 = grid[3][5], g28 = grid[3][6], g29 = grid[4][0], g30 = grid[4][1], g31 = grid[4][2], g32 = grid[4][3], g33 = grid[4][4], g34 = grid[4][5], g35 = grid[4][6], g36 = grid[5][0], g37 = grid[5][1], g38 = grid[5][2], g39 = grid[5][3],  g40 = grid[5][4], g41 = grid[5][5], g42 = grid[5][6], g43 = grid[6][0], g44 = grid[6][1], g45 = grid[6][2], g46 = grid[6][3], g47 = grid[6][4], g48 = grid[6][5], g49 = grid[6][6])
    else:
        flash('access denied! Please login first!')
        return redirect(url_for('Login'))

@app.route('/index/pd/<username>', methods=['GET', 'POST'])
def personal(username):
    user=User.query.filter_by(username=username).first()
    return render_template('personal.html', username = user.username, email = user.email)

@app.route('/UserConfirmation/<username>', methods=['GET','POST'])
def UserConfirmation(username):    
    user = User.query.filter_by(username=username).first()
    user.check=1
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('Login'))

@app.route('/Confirmation', methods=['GET','POST'])
def Confirmation():
    return '<h3> Mail sent!Please check your email id for the confirmation</h3>'

@app.route('/', methods=['GET', 'POST'])
def Start_Page():
    return render_template("start_page.html")

@app.route('/1', methods=['GET', 'POST'])
def Next_Page():
    return render_template("next_page.html")

@app.route('/Logout/<username>', methods=['GET', 'POST'])
def Logout(username):
    user=User.query.filter_by(username=username).first()
    user.log = 0
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('Login'))
if(__name__=="__main__"):
    manager.run()
