from flask import Flask, render_template,url_for, session
from InstagramAPI import InstagramAPI
import json
import fonctions
import os
import mysql.connector as mariadb

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
    userdb = conf["DB"]["USER"]
    pwddb = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]
    api = InstagramAPI(user,pwd)

    if api.login():
        api.getMediaLikers(mediaID)
        data3 = api.LastJson
        with open("data2.json", "w") as f:
            f.write(json.dumps(data3, indent=4)) 
        
        exemple = data3["users"][0]["full_name"]
        exemple1 = str(data3["users"][0]["pk"])
        #with open("log.txt", "w") as f:
        #    f.write(user)
        #    f.write(pwd)
        #    f.write(userdb)
        #    f.write(pwddb)
        #    f.write(db)
        #    f.write(mediaID)
        #    f.close()
        
        with open("log2.txt", "w") as fi:
            fi.write("exemple :")
            fi.write(exemple)
            fi.write("exemple1 :")
            fi.write(exemple1)
            fi.close()

        mariadb_connection = mariadb.connect(user= userdb, password=pwddb, database=db)        
        for i in range(10):
            cursor = mariadb_connection.cursor()
            cursor.execute("INSERT INTO `medias_likers`(`id`, `media_id`, `media_url`, `pk`, `username`, `fullname`, `isp`, `ppi`,`ppu`,`isv`,`latestmedia`) \
            VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (mediaID, url, data3["users"][i]["pk"], data3["users"][i]["username"],data3["users"][i]["full_name"],data3["users"][i]["is_private"],data3["users"][i]["profile_pic_url"],data3["users"][i]["profile_pic_id"],data3["users"][i]["is_verified"],data3["users"][i]["latest_reel_media"]))
            mariadb_connection.commit()
        
        mariadb_connection.close()        

    return render_template("index.html",user="succesfully inserted in DB !")

if __name__ == "__main__":
	MyApp.run()
