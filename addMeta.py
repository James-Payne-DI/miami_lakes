#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, selenium, urllib3, re, bs4, requests, csv, config, wpNavigation, sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen


#This program is to work with the page migration tool to migrate the meta separately from the other data
#This needed to be created because Yoast SEO does not work with REST API which is used for the rest of the data migration

#def manageScript():



def addPageMeta(backend_url,meta,driver):
    driver = wpNavigation.logInToDevsite(config.DRIVER_PATH,backend_url)

    #elem = driver.find_element_by_link_text("Edit Snippet")

    #Scroll the Yoast SEO box into view
    element = driver.find_element_by_id("wpseo_meta")
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)

    #Click Edit Snippet CTA
    elem = driver.find_element_by_xpath('//*[@id="wpseo-metabox-root"]/div[2]/div/div/section/div/button[1]')
    elem.click()

    time.sleep(0.15)

    #Find Text Box for description
    elem = driver.find_element_by_xpath('//*[@id="snippet-editor-field-description"]/div')
    time.sleep(0.15)
    elem.click()
    elem.send_keys(Keys.COMMAND, 'a')
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(meta)
    #print("Meta Sent")
    time.sleep(0.1)
    #//*[@id="wpseo-metabox-root"]/div[2]/div/div/section/div/section[2]/div[3]/div[2]/div[1]/div[1]
    #//*[@id="snippet-editor-field-description"]/div/div/div/span
    #

    #update the page.
    publish = driver.find_element_by_xpath("//*[@id='publish']")
    driver.execute_script("arguments[0].click();", publish)
    time.sleep(2)


    return driver
    # driver.close()


def testcreateBackendURL(dev_site, postID):
    backend_page_url = dev_site + 'wp/wp-admin/post.php?post='+ str(postID) +'&action=edit'
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
    try:
        driver_island.close()
        print("_"*50 + '\n' + "Meta Loop Complete")
        return
    except:
        error_message = "Bug Location=testMetaLoop()\n---» Issue Closing the web driver - please close it manually, thank you."
        print("_"*50 + '\n' + "Meta Loop Complete" + error_message)

# testMetaLoop("http://normreeveshondasuperstorenorthrichlandhills.dev.dealerinspire.com/")
# test_url = 'http://contentdevsandbox.dev.dealerinspire.com/wp/wp-admin/post.php?post=826&action=edit'
# test_meta = "TEST META DESCRIPTION"
# addPageMeta(test_url,test_meta)
