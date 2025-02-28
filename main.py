#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, time, json, base64, pprint, scrape, sqlite3, os, csv
import jsonFunctions, Live_Urls, config
from addMeta import addPageMeta
from format import formatMonth
from statusReports import GLOBAL_STATUS_REPORT as GSP
from statusReports import create_status_report

#TODO: Make this work for blogs. It should basically function the same but you'll need to scrape
#      date-of-publish, categrory, & tags

#createBackendURL - creates and returns the url of the backend of a page
def createBackendURL(dev_site, postID):
    backend_page_url = dev_site + 'wp/wp-admin/post.php?post='+ str(postID) +'&action=edit'
    return backend_page_url

def createCSVfromSQL(save_path, sql_file):
    conn = sqlite3.connect(sql_file)
    conn.execute("CREATE TABLE IF NOT EXISTS metaData (pageID INTEGER, pageTitle TEXT, slug TEXT, meta TEXT)")
    cursor = conn.cursor()
    cursor.execute("select * from metaData;")
    with open(save_path, 'w',newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    conn.close()

def urlDate(url):
    try:
        url = str(url)
        url_split = url.split('/')
        year = str(url_split[4])
        month = str(url_split[5])
        day = str(url_split[6])
        #Sanitize the date info
        if len(day) <= 1:
            day = '0' + day
        #turn month into a number but still a string
        month = formatMonth(month)
        date = year +'-'+ month +'-'+ day + 'T09:00:00'
        return str(date)
    except:
        return "2024-01-09T09:00:00"

#establishes the connection to the database within the variable db
#db = sqlite3.connect("metaHousing.sqlite")
#Creates the table metaData if one does not already exist
#db.execute("CREATE TABLE IF NOT EXISTS metaData (pageID INTEGER, pageTitle TEXT, slug TEXT, meta TEXT)")

#Deletes the metaHousing.sqlite file if one already exists
meta_csv_path = config.DESKTOP_PATH + '/' + config.dealership_name + '_' + 'previousRunReport.csv'
if os.path.exists("metaHousing.sqlite"):
    createCSVfromSQL(meta_csv_path, "metaHousing.sqlite")
    print(meta_csv_path)
    os.remove("metaHousing.sqlite")
    print("››› Existing version of 'metaHousing.sqlite' found, deleting it...")
else:
	print("››› The File Does Not already Exist")

# The devsite we are migrating the content to represented as a string
devsite = config.DEVSITE_URL

#Gets the User Input for the type of migration we are about to perform
type_of_run = input("Is this  for Blogs or Pages (blogs/pages)? ")

#Pulls the URLs we need
live_urls = Live_Urls.urlsToMigrate(config.GOOGLE_SHEET_ID)
#live_blogs = Live_Urls.urlsToMigrate(config.GOOGLE_SHEET_ID)





#First Loop For eash url in the google sheet - this loop creates each page in the list and adds all the data
#it also fills out metaData table which was created in line 17 above.



#Creates Database file and table
meta_db = open("metaHousing.sqlite", "x")
# print("››› sqlite file created & opened")
meta_db.close()
time.sleep(0.25)
db = sqlite3.connect("metaHousing.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS metaData (pageID INTEGER, pageTitle TEXT, slug TEXT, meta TEXT)")
# print("››› Connected to sqlite file -- metaData Table created")

if type_of_run == "pages":
    selectors = config.LIVE_SELECTOR_ID
    #PAGE MIGRATION LOOP
    for url in live_urls:
        scrape.livePage(url, selectors, devsite, db)
        time.sleep(2)
        db.commit()
elif type_of_run == "blogs":
    #selectors = config.LIVE_SELECTOR_ID[1]
    selectors = config.LIVE_SELECTOR_ID
    print("Blog Selectior______________________")
    print(selectors)
    #BLOG MIGRATION LOOP
    for url in live_urls:
        #url_date = urlDate(url)
        scrape.liveBlog(url, selectors, devsite, db)
        time.sleep(2)
        db.commit()
else:
    print("››› Issue with 'main.py' organization loop ...")
#close the database to be safe
db.close()

#Creates The Status Report .txt file and saves it to your desktop
create_status_report(GSP)


print("\n", "-"*40, "\n", "Meta Loop", "\n", "-"*40, "\n")


#set the connection to the database equal to "db"
db = sqlite3.connect("metaHousing.sqlite")

#loops through the metaData table line by line
meta_count = 0
driver = None
for page_id, name, slug, meta in db.execute("SELECT * FROM metaData"):
    if name == "404 - Page Not Found": continue
    backup_meta = "Learn more about {} on our website, or visit our dealership in %%di_city%%, %%di_state%%!".format(str(name))
    if meta == "": meta = backup_meta

    start = time.time()
    #do some stuff

    #1.) Create the backend URL with the ID and the dev site
    backend_url = createBackendURL(devsite, page_id)
    #print(backend_url)

    #2.) use method from addMeta with backend_url & meta as parameters
    meta_count +=1
    driver = addPageMeta(backend_url,meta,driver)
    print('››› ' + str(meta_count) + ': Meta Text Sent')

    #3.) all the meta should get  added it with the above command it exists  so when the loop closes the db link will close too
    stop = time.time()
    duration = stop-start
    print(duration)

    #4.) Close the Driver Window
    driver.quit()

config.MIGRATION_TYPE = str(type_of_run)
file_name = config.dealership_name + '_' + config.MIGRATION_TYPE + '_' 'runReport.csv'
meta_csv_path = config.DESKTOP_PATH + '/' + file_name
print(meta_csv_path)

if os.path.exists("metaHousing.sqlite"):
    createCSVfromSQL(meta_csv_path, "metaHousing.sqlite")
    os.remove("metaHousing.sqlite")
    print("››› Deleting 'metaHousing.sqlite' file that was created from this run ...")


print("«---------- Run Complete ----------»")
