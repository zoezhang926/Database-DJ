from flask import Flask, url_for, render_template, redirect, flash, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
# from models import db,connect_db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///djdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "itisasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# connect_db(app)

@app.route("/")
def home():
    return 'Create your own playlist'
if __name__ == '__main__':
  app.run(host='0.0.0.0')