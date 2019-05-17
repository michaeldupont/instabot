import os
import mysql.connector as mariadb
import json


def inputdb(media_likers):
    
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    username = conf["DB"]["USER"]
    pwd = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]

    mariadb_connection = mariadb.connect(user= username, password=pwd, database=db)
    cursor = mariadb_connection.cursor()
    
    cursor.execute( "INSERT INTO projet (nom, date_creation, cloture, responsable_id) \
                    SELECT \
                        projet.nom || ' Perso ' || utilisateur.prenom, CURRENT_TIMESTAMP, FALSE, projet.responsable_id \
                    FROM \
                    projet \
                    JOIN utilisateur ON utilisateur.id = projet.responsable_id \
                    WHERE projet.id IN (18, 42); \
                               ")

    mariadb_connection.commit()
    mariadb_connection.close()


def insertmedia(MediaID, MediaURL, likeCount, commentCount, pk, lieu):
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    
    userdb = conf["DB"]["USER"]
    pwd = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]

    mariadb_connection = mariadb.connect(user= userdb, password=pwd, database=db)
    cursor = mariadb_connection.cursor()

    cursor.execute( "INSERT IGNORE INTO `Media` (`id`, `MediaID`, `MediaURL`, `likeCount`, `commentCount`, `createTime`,`pk`,`lieu`,`updateTime`) \
                    VALUES (NULL, %s, %s,%s,%s,NULL,%s,%s,NULL)", (MediaID, MediaURL, likeCount, commentCount, pk, lieu))
                               
    mariadb_connection.commit()
    mariadb_connection.close()

def readmedia(MediaID):
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    
    userdb = conf["DB"]["USER"]
    pwd = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]

    sql = "SELECT * from `Media` WHERE `id`= " + str(MediaID) 

    mariadb_connection = mariadb.connect(user= userdb, password=pwd, database=db)
    cursor = mariadb_connection.cursor()

    cursor.execute(sql)
    result = cursor.fetchall()
                               
    mariadb_connection.close()
    return result

def readAllMedia():
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    
    userdb = conf["DB"]["USER"]
    pwd = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]

    sql = "SELECT * from `Media`" 

    mariadb_connection = mariadb.connect(user= userdb, password=pwd, database=db)
    cursor = mariadb_connection.cursor()

    cursor.execute(sql)
    result = cursor.fetchall()
                               
    mariadb_connection.close()
    return result

def insertpeople(pk,username,full_name,compjson):
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    
    userdb = conf["DB"]["USER"]
    pwd = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]

    mariadb_connection = mariadb.connect(user= userdb, password=pwd, database=db)
    cursor = mariadb_connection.cursor()
    
    cursor.execute( "INSERT INTO `People`(`id`, `pk`, `username`, `full_name`, `compjson`) \
                    VALUES (NULL,%s, %s,%s,%s)", (pk, username, full_name, compjson))
    mariadb_connection.commit()
    mariadb_connection.close()


def linkMP(MediaID, pk):
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    
    userdb = conf["DB"]["USER"]
    pwd = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]

    mariadb_connection = mariadb.connect(user= userdb, password=pwd, database=db)
    cursor = mariadb_connection.cursor()
    
    cursor.execute( "INSERT INTO Media_likers () \
                    VALUES () \
                               ")
    mariadb_connection.commit()
    mariadb_connection.close()