from flask import Flask, url_for, render_template, redirect, flash, jsonify, request,session
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
# from models import db,connect_db,loginForm
from form import LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///djdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "itisasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

debug = DebugToolbarExtension(app)

# connect_db(app)

@app.route('/')
def login():
  form = LoginForm()
  return render_template('Formlogin.html', title='Sign In', form=form)

if __name__ == '__main__':
  app.run(host='0.0.0.0')