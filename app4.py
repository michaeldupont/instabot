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
        
        exemple = str(data3["users"][0]["full_name"])
        exemple1 = str(data3["users"][0]["pk"])
        with open("log3.txt", "w") as f:
            f.write(userdb + '\n')
            f.write(pwddb + '\n')
            f.write(db + '\n')
            f.write(mediaID)
            f.close()
        
        mariadb_connection = mariadb.connect(user=userdb, password=pwddb, database=db)
        with open("log4.txt", "w") as fi:
            fi.write("ok" + '\n')
            fi.close()

        for i in range(10):
            cursor = mariadb_connection.cursor()
            with open("log4.txt", "w") as fi:
                fi.write("ok1" + "\n")
                fi.write(str(mediaID) + "\n")
                fi.write(str(url) + "\n")
                fi.write(str(data3["users"][i]["pk"]) + "\n")
                fi.write(str(data3["users"][i]["username"] + "\n")
                fi.write(str(data3["users"][i]["is_private"]) + "\n")            
                fi.close()

            cursor.execute("INSERT INTO `medias_likers`(`id`, `media_id`, `media_url`, `pk`, `username`, `fullname`, `isp`, `ppi`,`ppu`,`isv`,`latestmedia`) \
            VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (str(mediaID), str(url), str(data3["users"][i]["pk"]), str(data3["users"][i]["username"]),str(data3["users"][i]["full_name"]),str(data3["users"][i]["is_private"]),str(data3["users"][i]["profile_pic_url"]),str(data3["users"][i]["profile_pic_id"]),str(data3["users"][i]["is_verified"]),str(data3["users"][i]["latest_reel_media"])))
            mariadb_connection.commit()
            with open("log4.txt", "w") as fi:
                fi.write("ok2")
                fi.close()
        
        mariadb_connection.close()        

    return render_template("index.html",user="succesfully inserted in DB !")

if __name__ == "__main__":
	MyApp.run()
