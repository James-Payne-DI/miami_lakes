#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, time, json, jsonFunctions, base64, pprint, Live_Urls, scrape, sqlite3
from addMeta import addPageMeta

#TODO: Make this work for blogs. It should basically function the same but you'll need to scrape
#      date-of-publish, categrory, & tags

#createBackendURL - creates and returns the url of the backend of a page
def createBackendURL(dev_site, postID):
    backend_page_url = dev_site + 'wp/wp-admin/post.php?post='+ str(postID) +'&action=edit'
    return backend_page_url

#establishes the connection to the database within the variable db
db = sqlite3.connect("metaHousing.sqlite")
#Creates the table metaData if one does not already exist
db.execute("CREATE TABLE IF NOT EXISTS metaData (pageID INTEGER, pageTitle TEXT, slug TEXT, meta TEXT)")

#devsite we are migrating the content to
devsite = 'http://contentdevsandbox.dev.dealerinspire.com/'



#the id for the google sheet we get the list of links from
live_urls = Live_Urls.urlsToMigrate('1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko')

#live_blogs = Live_Urls.urlsToMigrate('1nayRdiuQUQcvHK5LYA_CoEYpNPuHKdS2ybhdmY_cxS0')
#'19fSBX26VrTMT5u9n34t0PWrT1Bnx-nYPckTpd3M1LtY')
#blog1


test_run = input("Is this  a test run (y/n)? ")

#First Loop For eash url in the google sheet - this loop creates each page in the list and adds all the data
#it also fills out metaData table which was created in line 17 above.
for url in live_urls:
    scrape.livePage(url, 'fullcontentrow', devsite, db)
    time.sleep(2)
    db.commit()

#close the database to be safe
db.close()


print("\n", "-"*40, "\n", "Meta Loop", "\n", "-"*40, "\n")


#set the connection to the database equal to "db"
db = sqlite3.connect("metaHousing.sqlite")

#loops through the metaData table line by line
for page_id, name, slug, meta in db.execute("SELECT * FROM metaData"):
    #1.) Create the backend URL with the ID and the dev site
    backend_url = createBackendURL(devsite, page_id)
    #print(backend_url)

    #2.) use method from addMeta with backend_url & meta as parameters
    addPageMeta(backend_url,meta)

    #3.) all the meta should get  added it with the above command it exists  so when the loop closes the db link will close too


if test_run == "y":
    #Connecting to sqlite
    conn = sqlite3.connect('metaHousing.sqlite')
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #Doping EMPLOYEE table if already exists
    cursor.execute("DROP TABLE metaData")
    print("Table dropped... rowcount is: ", cursor.rowcount)
    #Commit your changes in the database
    conn.commit()
    #Closing the connection
    conn.close()
