from flask import Flask, render_template,url_for, session
from InstagramAPI import InstagramAPI
import json
import fonctions
import os
import database
import pandas as pd
import matplotlib.pyplot as plt

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

@MyApp.route('/read')
def read():
    id = 30
    result1 = database.readmedia(id)
    result2 = database.readAllMedia()
    
    df = pd.DataFrame(result2, columns=["id", "MediaID", "MediaURL", "likeCount", "commentCount", "createTime","pk","lieu","updateTime"])
    x = df.MediaID
    y = df.likeCount
    plt.scatter(x, y)
    plt.savefig("first.png")

    with open("log10.txt", "a") as fi:
            fi.write("ok" + "\n")
            fi.write(str(result1) + "\n")
            fi.write(str(result1[2]) + "\n")
            fi.write(str(result1[0][2]) + "\n")        
            fi.close()

    return render_template("media.html", image1=str(result1[0][2]))

@MyApp.route("/data")
def data():
    with open("config.json","r") as fichier:
        conf = json.load(fichier)
    user = conf["INSTAGRAM"]["USER"]
    pwd = conf["INSTAGRAM"]["PASSWORD"]
    api = InstagramAPI(user,pwd)
    
    if api.login():
    # recuperation des medias changer pour les recuperer tous
        api.getSelfUserFeed()
        data = api.LastJson
        with open("log7.txt", "w") as fi:
            fi.write("ok" + "\n")

    # test sur le fichier JSON deja logge pour ne pas solliciter l'API
    with open("getSelfUserFeed.json","r") as fichier:
        data = json.load(fichier)
    
    #    with open("getSelfUserFeed.json", "w") as f:
    #        f.write(json.dumps(data, indent=4))


    #    with open("log7.txt", "a") as fi:
    #        fi.write("ok" + "\n")
    #        fi.write(str(data["items"]) + "\n")
    #        fi.write(str(data["next_max_id"]) + "\n")        
    #        fi.close()

    # insertion des media dans la table media
    for item in data["items"]:
        #on insere pour le moment mais il faudrait d'abord lire en base pour comparer si element existe ou pas ... s'il existe, faut il update ?
        
        if "location" in item:
            var = item["location"]["name"]
        else:
            var = "0"
       
        database.insertmedia(item["id"], item["image_versions2"]["candidates"][0]["url"], item["like_count"], item["comment_count"], item["pk"], var)
              
    return render_template("index.html", user="va voir le log7.txt")

@MyApp.route("/bytel")
def MediaData():
    url = "https://www.instagram.com/p/BwToC2vnz9H/"
    mediaID = fonctions.get_media_id(url)

    with open("config.json","r") as fichier:
        conf = json.load(fichier)
    userdb = conf["INSTAGRAM"]["USER"]
    pwd = conf["INSTAGRAM"]["PASSWORD"]

    api = InstagramAPI(userdb,pwd)

    if api.login():
        api.getMediaLikers(mediaID)
        data3 = api.LastJson
        # database.insertmedia(mediaID,url,data3["user_count"])
                       
        for user in range(data3["user_count"]):
            datauser = data3["users"][user]

            with open("log5.txt", "w") as fi:
                fi.write("here ! cle : valeur" + "\n")
                fi.write(str(datauser) + "\n")
                fi.write(str(datauser["pk"]) + "\n")        
                fi.close()

            database.insertpeople(datauser["pk"],datauser["username"],datauser["full_name"],datauser)
            #database.linkMP(mediaID,datavaleur[0])   linker la table avec les cles primaires ??   attention bdd change donc modifier

    return render_template("index.html",user="succesfully inserted in DB !")

if __name__ == "__main__":
	MyApp.run()


