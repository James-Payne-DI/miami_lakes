#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, urllib3, re, requests, csv, sqlite3, os

import selenium, bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen

import config, wpNavigation, findby

#This program is to work with the page migration tool to migrate the meta separately from the other data
#This needed to be created because Yoast SEO does not work with REST API which is used for the rest of the data migration

#def manageScript():



def addPageMeta(backend_url,meta,driver):
    try:
        driver = wpNavigation.logInToDevsite(config.DRIVER_PATH,backend_url)
    except:
        print("_♦_| Quick Login failed » Trying Slow Login____________________")
        try:
            driver = wpNavigation.logInToDevsite_slower(config.DRIVER_PATH,backend_url)
        except:
            print("_♦_| Slow Login failed » Check Inputs____________________")
            driver.quit()
            return driver
        else:
            print("_♦_| Slow Login worked____________________")


    element = None
    try:
        find_yoast_box(driver)
    except:
        print("_♦_| --yoast attempt 1-- FAILED")
        try:
            find_yoast_box(driver)
        except:
            print("_♦_| --yoast attempt 2-- FAILED")
            driver.quit()
            return driver
        else:
            print("_♦_| --yoast attempt 2-- SUCCESS")
    else:
        print("_♦_| OG selector  --yoast attempt 1-- SUCCESS")


    time.sleep(0.35)

    #Find Text Box for description
    elem = driver.find_element_by_xpath('//*[@id="snippet-editor-field-description"]/div')
    time.sleep(0.35)
    elem.click()
    elem.send_keys(Keys.COMMAND, 'a')
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(meta)
    #print("Meta Sent")
    time.sleep(0.35)
    #//*[@id="wpseo-metabox-root"]/div[2]/div/div/section/div/section[2]/div[3]/div[2]/div[1]/div[1]
    #//*[@id="snippet-editor-field-description"]/div/div/div/span
    #

    #update the page.
    publish = driver.find_element_by_xpath("//*[@id='publish']")
    driver.execute_script("arguments[0].click();", publish)
    time.sleep(3.5)


    return driver
    # driver.close()



def find_yoast_box(driver):
    # element = findyby.clickableId(driver, "wpseo_meta")
    element = driver.find_element_by_id("wpseo_meta")
    time.sleep(0.35)
    #Scroll the Yoast SEO box into view
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    if "closed" in str(element.get_attribute("class")):
        element.click()
        time.sleep(0.35)
    #Click Edit Snippet CTA
    elem = driver.find_element_by_xpath('//*[@id="wpseo-metabox-root"]/div[2]/div/div/section/div/button[1]')
    time.sleep(0.35)
    elem.click()
    return driver


def testcreateBackendURL(dev_site, postID):
    backend_page_url = dev_site + 'wp/wp-admin/post.php?post='+ str(postID) +'&action=edit'
    print(backend_page_url)
    return backend_page_url



def testMetaLoop(devsite):
    #set the connection to the database equal to "db"
    db = sqlite3.connect("metaHousing.sqlite")

    #loops through the metaData table line by line
    full_meta_count = 0
    reset_counter = 0
    driver_island = None
    for page_id, name, slug, meta in db.execute("SELECT * FROM metaData"):
        start = time.time()
        #do some stuff

        #1.) Create the backend URL with the ID and the dev site
        backend_url = testcreateBackendURL(devsite, page_id)
        #print(backend_url)

        #2.) use method from addMeta with backend_url & meta as parameters
        full_meta_count +=1

        driver_island = addPageMeta(backend_url,meta,driver_island)
        print(str(full_meta_count) + ': Meta Text Sent')
        reset_counter += 1
        if reset_counter == 5: reset_counter = 0


        #3.) all the meta should get  added it with the above command it exists  so when the loop closes the db link will close too
        stop = time.time()
        duration = stop-start
        print(duration)
        driver_island.quit()
    try:
        driver_island.quit()
        print("_"*50 + '\n' + "Meta Loop Complete")
        return
    except:
        error_message = "Bug Location=testMetaLoop()\n---» Issue Closing the web driver - please close it manually, thank you."
        print("_"*50 + '\n' + "Meta Loop Complete" + error_message)

def createCSVfromSQL(save_path, sql_file):
    conn = sqlite3.connect(sql_file)
    cursor = conn.cursor()
    cursor.execute("select * from metaData;")
    with open(save_path, 'w',newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    conn.close()



def deletePost(backend_url):
    driver = wpNavigation.logInToDevsite(config.DRIVER_PATH,backend_url)

    #elem = driver.find_element_by_link_text("Edit Snippet")
    time.sleep(2)

    #click move to trash
    elem = driver.find_element_by_xpath('//*[@id="delete-action"]/a')
    elem.click()
    time.sleep(2)

    driver.quit()

def deletePosts(devsite):
    file_name = config.dealership_name + '_' + 'runReport.csv'
    meta_csv_path = config.DESKTOP_PATH + '/' + file_name
    print(meta_csv_path)

    if os.path.exists("metaHousing.sqlite"):
        createCSVfromSQL(meta_csv_path, "metaHousing.sqlite")
        print("_♦_| Creating File {}   ......".format(file_name))
    db = sqlite3.connect("metaHousing.sqlite")
    meta_count = 0
    driver = None
    last_post_id = 0
    asset_id_list = []
    for post_id, name, slug, meta in db.execute("SELECT * FROM metaData"):
        #1.) Create the backend URL with the ID and the dev site

        try:
            backend_url = testcreateBackendURL(devsite, post_id)
            #print(backend_url)
            driver = deletePost(backend_url)
            print(str(meta_count) + '_♦_|' + ': Post Deleted - ID: {}'.format(post_id))
            #2.) use method from addMeta with backend_url & meta as parameters
            meta_count +=1
        except:
            print(str(meta_count) + '_♦_|' + 'FAILURE to delete post - ID: {}'.format(post_id))
            meta_count +=1
    print("¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬deletePosts(devsite) complete¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬")

def reRunMetaLoop(devsite, starter):
    #loops through the metaData table line by line
    starter = int(starter)
    file_name = config.dealership_name + '_' + 'runReport.csv'
    meta_csv_path = config.DESKTOP_PATH + '/' + file_name
    print(meta_csv_path)

    if os.path.exists("metaHousing.sqlite"):
        createCSVfromSQL(meta_csv_path, "metaHousing.sqlite")
        print("_♦_| Creating File {}   ......".format(file_name))
    db = sqlite3.connect("metaHousing.sqlite")
    meta_count = 0
    driver = None
    for page_id, name, slug, meta in db.execute("SELECT * FROM metaData"):
        print("Starter: ", str(starter))
        print("Page Count: ", str(meta_count))
        if meta_count < starter:
            meta_count +=1
            continue
        if not page_id:
            continue
        if name == "404 - Page Not Found": continue
        start = time.time()
        #do some stuff

        #1.) Create the backend URL with the ID and the dev site
        backend_url = testcreateBackendURL(devsite, page_id)
        #print(backend_url)

        #2.) use method from addMeta with backend_url & meta as parameters
        meta_count +=1
        driver = addPageMeta(backend_url,meta,driver)
        print('_♦_| ' + str(meta_count) + ': Meta Text Sent')

        #3.) all the meta should get  added it with the above command it exists  so when the loop closes the db link will close too
        stop = time.time()
        duration = stop-start
        print(duration)

        #4.) Close the Driver Window
        driver.quit()
    if os.path.exists("metaHousing.sqlite"):
        os.remove("metaHousing.sqlite")
        print("_♦_| Deleting 'metaHousing.sqlite' file that was created from this run ...")


# reRunMetaLoop("https://miamilakesautomall.dev.dealerinspire.com/", 0)
# test_url = 'http://contentdevsandbox.dev.dealerinspire.com/wp/wp-admin/post.php?post=826&action=edit'
# test_meta = "TEST META DESCRIPTION"
# addPageMeta(test_url,test_meta)
# file_name = config.dealership_name + '_' + 'runReport.csv'
# meta_csv_path = config.DESKTOP_PATH + '/' + file_name
# createCSVfromSQL(meta_csv_path, "metaHousing.sqlite")
#deletePosts("https://miamilakesautomall.dev.dealerinspire.com/")
