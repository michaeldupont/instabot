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


def insertmedia(MediaID, MediaURL, nbr_likers):
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    
    username = conf["DB"]["USER"]
    pwd = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]

    mariadb_connection = mariadb.connect(user= username, password=pwd, database=db)
    cursor = mariadb_connection.cursor()

    cursor.execute( "INSERT IF NOT EXISTS INTO `Media` (`ìd`, `MediaID`, `MediaURL`, `nbr_likers`) \
                    VALUES (NULL, %s, %s,%s)(MediaID, MediaURL, nbr_likers) \
                               ")
    mariadb_connection.commit()
    mariadb_connection.close()

def insertpeople(pk,username,full_name,compjson):
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    
    username = conf["DB"]["USER"]
    pwd = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]

    mariadb_connection = mariadb.connect(user= username, password=pwd, database=db)
    cursor = mariadb_connection.cursor()
    
    cursor.execute( "INSERT INTO `People` (`pk`, `username`, `full_name`,`compjson`) \
                    VALUES (pk, username,full_name,compjson) \
                               ")
    mariadb_connection.commit()
    mariadb_connection.close()


def linkMP(MediaID, pk):
    with open("config.json","r") as fichier:
        conf = json.load(fichier) 
    
    username = conf["DB"]["USER"]
    pwd = conf["DB"]["PASSWORD"]
    db = conf["DB"]["DATABASE"]

    mariadb_connection = mariadb.connect(user= username, password=pwd, database=db)
    cursor = mariadb_connection.cursor()
    
    cursor.execute( "INSERT INTO Media_likers () \
                    VALUES () \
                               ")
    mariadb_connection.commit()
    mariadb_connection.close()