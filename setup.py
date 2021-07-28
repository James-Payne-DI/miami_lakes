#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, scrape, time, selenium, findby, urllib.request, config
from requests_html import HTMLSession
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

request_headers = {'User-Agent': 'Mozilla/5.0'}
all_page_titles = []
blog_page_titles = []
print('Setup Squad in Action')
def headlessLogin(site, username=config.DEVSITE_USERNAME, password=config.DEVSITE_PASSWORD):
    print('headlessLogin engaged')
    site = site + 'wp/wp-login.php'
    session = createSession()
    login = session.get(site, headers=request_headers)
    soup = scrape.makeSoup(login.content)
    form = scrape.makeForm(soup, username, password)
    login_response = session.post(site, data=form)
    return session

def createSession():
    session = requests.session()
    return session

def createBackendURL(live_site, postID):
    backend_page_url = live_site + 'wp/wp-admin/post.php?post='+ postID +'&action=edit'
    return backend_page_url

def createBackendSoup(session, live_site, postID):
    backend_page = session.get(createBackendURL(live_site, postID), headers=request_headers)
    soup = scrape.makeSoup(backend_page.content)
    return soup

def requestHTML(url):
    request_html = formatRequest(url)
    opener = urllib.request.build_opener()
    page = opener.open(request_html)
    return page

def formatRequest(url):
    req = urllib.request.Request(url, headers=request_headers)
    return req

#*******************************SELENIUM DEVSITE NAVIGATION************************
def createDriver(driver_path):
    driver = webdriver.Chrome(driver_path)
    return driver

def toDevsite(driver, dev_site):
    driver.get(dev_site)
    time.sleep(2)
    return driver

def loginToDevSite(dev_site, username=config.DEVSITE_USERNAME, password=config.DEVSITE_PASSWORD):
    driver = createDriver('/Users/jimmypayne/Documents/chromedriver')
    dev_site = dev_site + 'wp/wp-admin'
    driver = toDevsite(driver, dev_site)
    driver = fillUserField(driver, username)
    driver = fillPasswordField(driver, password)
    driver = submitLogin(driver)
    driver = toAllPages(driver)
    #driver = setScreenOptions(driver)

    return driver

def toMediaLibrary(driver):
    media_library = findby.clickableXpath(driver, '//*[@id="menu-media"]/a')
    executeJavaScript(driver, javascriptClick(), media_library)
    try:
        list_view = findby.clickableXpath(driver, '//*[@id="wp-media-grid"]/div[3]/div[4]/div/div[3]/div[1]/div/a[1]')
        executeJavaScript(driver, javascriptClick(), list_view)
        driver = setScreenOptions(driver)
        return driver
    except TimeoutException:
        list_view = findby.clickableId(driver, 'view-switch-list')
        executeJavaScript(driver, javascriptClick(), list_view)
        driver = setScreenOptions(driver)
        return driver

def setScreenOptions(driver):
    screen_options = findby.clickableId(driver, 'show-settings-link')
    executeJavaScript(driver, javascriptClick(), screen_options)
    try:
        page_count = findby.visibleID(driver, 'edit_page_per_page')
    except TimeoutException:
        page_count = findby.visibleID(driver, 'upload_per_page')
    finally:
        page_count.clear()
        page_count.send_keys(999)
        submit = findby.visibleID(driver, 'screen-options-apply')
        executeJavaScript(driver, javascriptClick(), submit)
        return driver

def fillUserField(driver, username):
    user_field = findby.clickableId(driver, "user_login")
    user_field.click()
    user_field.send_keys(username)
    return driver

def fillPasswordField(driver, password):
    password_field = findby.clickableId(driver, "user_pass")
    password_field.click()
    password_field.send_keys(password)
    return driver

def submitLogin(driver):
    submitButton = findby.clickableXpath(driver, "//*[@id='wp-submit']")
    submitButton.click()
    return driver

def toAllPages(driver):
    pages_link = findby.clickableXpath(driver, '//*[@id="menu-pages"]/a/div[3]')
    #executeJavaScript(driver, javascriptClick(), pages_link)
    pages_link.click()
    driver = findby.auditorCheck(driver)
    return driver

def toPage(driver, link_text):
    page_link = findby.clickableLinkText(driver, link_text)
    page_link.click()
    return driver

def addLightningSeo(driver, seo_content):
    content_box = findby.visibleID(driver, "lvrpSeoContentEditor")
    content_box.clear()
    executeJavaScript(driver, javascriptChangeValueOfElement(), content_box, seo_content)
    return driver

def chooseTemplate(driver, template):
    dropdown = findby.selectByVisibleID(driver, "page_template")
    driver = findby.makeSelection(driver, dropdown, template)
    return driver

def chooseParent(driver, value):
    dropdown = findby.selectByVisibleID(driver, "parent_id")
    driver = findby.makeSelection(driver, dropdown, value)
    return driver

def addNew(driver):
    add_new_button = findby.clickableXpath(driver, '//*[@id="wpbody-content"]/div[3]/a')
    executeJavaScript(driver, javascriptClick(), add_new_button)
    return driver

def addPageTitle(driver, page_title):
    titleField =  findby.visibleID(driver, "title")
    executeJavaScript(driver, javascriptChangeValueOfElement(), titleField, page_title)
    return driver

def publish(driver):
    publish_button = findby.clickableXpath(driver, "//*[@id='publish']")
    executeJavaScript(driver, javascriptClick(), publish_button)

    return driver

def executeJavaScript(driver, javascript, *args):
    driver.execute_script(javascript, *args)

def javascriptClick():
    code = "arguments[0].click();"
    return code

def javascriptChangeValueOfElement():
    code = "arguments[0].value=arguments[1];"
    return code

def vrpPage(driver, title, template):
    driver = addPageTitle(driver, title)
    driver = chooseTemplate(driver, template)
    driver = publish(driver)
    return driver

def usedVrpPage(driver, title, template):
    driver = addPageTitle(driver, title)
    driver = chooseParent(driver, '7')
    driver = chooseTemplate(driver, template)
    driver = publish(driver)
    return driver

def newVrpPage(driver, title, template):
    driver = addPageTitle(driver, title)
    driver = chooseParent(driver, '6')
    driver = chooseTemplate(driver, template)
    driver = publish(driver)
    return driver

def addContent(driver, soup):
    content = "\n".join(scrape.vrpContent(soup))
    driver = addLightningSeo(driver, content)
    driver = publish(driver)
    return driver

def addDipcRows(driver, num_of_wysiwyg):
    #Create 'num_of_wysiwyg' number of WYSIWYGs
    for i in range(num_of_wysiwyg):
        add_row = findby.presenceOfXpathIgnoreExceptions(driver, '//*[@id="acf-group_554d290c123aa"]/div/div[1]/div[2]/div/div[4]/a')
        add_row.click()
        #elem = findby.clickableXpath(driver, "//*[@id='acf-group_554d290c123aa']/div/div[1]/div[2]/div/div[4]/a")
        #driver.execute_script("arguments[0].click();", elem)

        elem = driver.find_element_by_xpath("/html/body/div[9]/ul/li[1]/a")
        driver.execute_script("arguments[0].click();", elem)
    return driver

def addValuesToDipcRows(driver, acfs_and_values):
    for value in acfs_and_values:
        #print(value)
        acf = findby.presenceOfId(driver, value)
        executeJavaScript(driver, javascriptChangeValueOfElement(), acf, acfs_and_values[value])
    return driver

def checkMaxWidth(driver, max_width_checked):
    for checked in max_width_checked:
        checkbox = findby.presenceOfId(driver, checked)
        executeJavaScript(driver, javascriptClick(), checkbox)
    return driver


def addCSS(driver, css_content):
    css_override_box = findby.clickableXpath(driver, "//*[@id='acf-group_554d290c123aa']/div/div[2]/div[2]/div/div[6]/div[1]/div/div/div/div[5]/div/pre")
    css_override_box.click()
    css_textarea = findby.presenceOfXpath(driver, '//*[@id="acf-group_554d290c123aa"]/div/div[2]/div[2]/div/div[1]/textarea')
    executeJavaScript(driver, javascriptChangeValueOfElement(), css_textarea, css_content)
    driver = publish(driver)

    return driver
