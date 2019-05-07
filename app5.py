# last update : mariaDB 10.2 and JSON store JSON object in mariaDB 
# connection à la base avec mysql --user=chnordfr --password= 'lememequedans la console'  

from flask import Flask, render_template,url_for, session
from InstagramAPI import InstagramAPI
import json
import fonctions
import os
import database

MyApp = Flask(__name__)
# Config options - Make sure you created a 'config.py' file.
MyApp.config.from_object('config')
# To get one variable, tape MyApp.config['MY_VARIABLE']

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
    url = "https://www.instagram.com/p/BwToC2vnz9H/"
    mediaID = fonctions.get_media_id(url)

    if api.login():
        api.getMediaLikers(mediaID)
        data3 = api.LastJson
        with open("data3.json", "w") as f:
            f.write(json.dumps(data3, indent=4))
        
    return render_template("index.html")

@MyApp.route("/bytel")
def MediaData():
    url = "https://www.instagram.com/p/BwToC2vnz9H/"
    mediaID = fonctions.get_media_id(url)

    with open("config.json","r") as fichier:
        conf = json.load(fichier)
    user = conf["INSTAGRAM"]["USER"]
    pwd = conf["INSTAGRAM"]["PASSWORD"]

    api = InstagramAPI(user,pwd)

    if api.login():
        api.getMediaLikers(mediaID)
        data3 = api.LastJson
                       
        for user in range(data3["user_count"]):
            datauser = data3["users"][user]
            # idéalement ne garder que les données qui ne sont pas pk, username, full_name et profilpicture et profileid

            for cle,valeur in data3["users"][user].items():

                with open("log5.txt", "w") as fi:
                    fi.write("i'm here" + "\n")
                    fi.close()

                datacle = []
                datavaleur = []
                datacle.append(cle)
                datavaleur.append(valeur)

                database.insertmedia(mediaID,url,data3["user_count"])
                #database.insertpeople(datavaleur[0],datavaleur[1],datavaleur[2],datauser)
                #database.linkMP(mediaID,datavaleur[0])      

    return render_template("index.html",user="succesfully inserted in DB !")

if __name__ == "__main__":
	MyApp.run()


