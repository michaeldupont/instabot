from flask import Flask, render_template,url_for, session
from InstagramAPI import InstagramAPI
import json
import fonctions
from InstagramAPI import InstagramAPI
from flask_sqlalchemy import SQLAlchemy

MyApp = Flask(__name__)
# Config options - Make sure you created a 'config.py' file.
MyApp.config.from_object('config')
# To get one variable, tape MyApp.config['MY_VARIABLE']
MyApp.config['SQLALCHEMY_DATABASE_URI'] = "localhost"
db = SQLAlchemy(MyApp)

class AddressBook(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    media_ID = db.Column(db.String(100))
    media_URL = db.Column(db.String(50))
    pk = db.Column(db.String(200))
    username = db.Column(db.String(10))
    full_name = db.Column(db.String(10))
    is_private = db.Column(db.boolean())
    profile_pic_url = db.Column(db.String(200))
    profile_pic_id = db.Column(db.String(200))
    is_verified = db.Column(db.boolean())

    def __init__(self, name, city, addr, pin):
        self.media_ID = media_ID
        self.city = media_URL
        self.addr = pk
        self.pin = username
        self.media_ID = full_name
        self.city = is_private
        self.addr = profile_pic_url
        self.pin = is_verified


@MyApp.route("/")
def hello():
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    username = conf["INSTAGRAM"]["USER"]
    # 
    return render_template("index.html", user=username)

@MyApp.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@MyApp.route("/data")
def data():
    with open("config.json","r") as fichier:
        conf = json.load(fichier)
    user = conf["INSTAGRAM"]["USER"]
    pwd = conf["INSTAGRAM"]["PASSWORD"]
    api = InstagramAPI(user,pwd)

    if api.login():
        api.getSelfUserFeed()
        data1 = api.LastJson
        with open("data1.json", "w") as f:
            f.write(json.dumps(data1, indent=4))
            #test sur git branche de test
        
    return render_template("index.html")

@MyApp.route("/bytel")
def MediaData():
    url = "https://www.instagram.com/p/BwToC2vnz9H/"
    mediaID = fonctions.get_media_id(url)


    return render_template("index.html")

if __name__ == "__main__":
	MyApp.run()
