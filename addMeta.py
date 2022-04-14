#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, selenium, urllib3, re, bs4, requests, csv, config
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen


#This program is to work with the page migration tool to migrate the meta separately from the other data
#This needed to be created because Yoast SEO does not work with REST API which is used for the rest of the data migration


def addPageMeta(backend_url,meta):
    #Username
    user = config.DEVSITE_USERNAME
    #raw_input("Enter Username: ")

    #Password
    pwd = config.DEVSITE_PASSWORD
    #raw_input("Enter Password: ")

    #name for di auditor
    name = 'Jimbos Robot'
    #raw_input("Enter Your Name: ")

    #path to chrome driver
    driverpath = "/Users/jimmypayne/Documents/chromedriver"
    #raw_input("Path to Chrome Driver: ")
    driver = webdriver.Chrome(driverpath)

    #Dev-Site
    #devsite = "http://kendallautowashington.dev.dealerinspire.com/wp/wp-admin/"
    #raw_input("Enter Dev-Site URL: ")

    #open devsite
    driver.get(backend_url)
    time.sleep(2)

    #have driver enter Username
    elem = driver.find_element_by_id("user_login")
    elem.send_keys(user)

    #have driver enter password
    elem = driver.find_element_by_id("user_pass")
    elem.send_keys(pwd)

    #Click log in button.
    driver.find_element_by_xpath("//*[@id='wp-submit']").click()

    #enter Developer name for DI auditor
    elm = driver.find_elements_by_xpath("//*[@id='user']")
    if len(elm) > 0:
        elem = driver.find_element_by_xpath("//*[@id='user']")
        elem.send_keys(name)
        elem = driver.find_element_by_xpath("//*[@id='form--di-audit-log-name']/div/div[2]/div/fieldset/div[2]/input")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(2)

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

    driver.close()

# test_url = 'http://contentdevsandbox.dev.dealerinspire.com/wp/wp-admin/post.php?post=826&action=edit'
# test_meta = "TEST META DESCRIPTION"
# addPageMeta(test_url,test_meta)
