#!/usr/bin/env python3

import selenium, time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def waitUntil(driver, condition, selector, selection, *args):
    if len(args) == 0:
        driver = WebDriverWait(driver, 10).until(condition(selector, selection))
        return driver
    else:
        driver = WebDriverWait(driver, 20, ignored_exceptions=ignoreExceptions()).until(condition(selector, selection))
        return driver

def ignoreExceptions():
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
    return ignored_exceptions

def presenceOfXpathIgnoreExceptions(driver, xpath):
    element = waitUntil(driver, presenceLocated, By.XPATH, xpath, 'ignore')
    return element

def presenceOfNameIgnoreExceptions(driver, name):
    element = waitUntil(driver, presenceLocated, By.NAME, name, 'ignore')
    return element

def presenceOfAllTagNamesIgnoreExceptions(driver, tag_name):
    elements = waitUntil(driver, presenceOfAllLocated, By.TAG_NAME, tag_name, 'ignore')
    return elements

def presenceOfAllXpath(driver, xpath):
    elements = waitUntil(driver, presenceOfAllLocated, By.XPATH, xpath)
    return elements

def clickableId(driver, id):
    element = waitUntil(driver, clickable, By.ID, id)
    return element

def clickableXpath(driver, xpath):
    element = waitUntil(driver, clickable, By.XPATH, xpath)
    return element

def clickableClassName(driver, class_name):
    element = waitUntil(driver, clickable, By.CLASS_NAME, class_name)
    return element

def clickableCSS(driver, css):
    element = waitUntil(driver, clickable, By.CSS, css)
    return element

def visibleID(driver, id):
    element =  waitUntil(driver, visible, By.ID, id)
    return element

def visibleXpath(driver, xpath):
    element = waitUntil(driver, visible, By.XPATH, xpath)
    return element

def presenceOfId(driver, id):
    element = waitUntil(driver, presenceLocated, By.ID, id)
    return element

def presenceOfXpath(driver, xpath):
    element = waitUntil(driver, presenceLocated, By.XPATH, xpath)
    return element

def clickableLinkText(driver, link_text):
    element = waitUntil(driver, clickable, By.LINK_TEXT, link_text)
    return element

def clickable(selector, selection):
    clickable = EC.element_to_be_clickable((selector, selection))
    return clickable

def visible(selector, selection):
    visible =  EC.visibility_of_element_located((selector, selection))
    return visible

def presenceOfAllLocated(selector, selection):
    all_elements_present = expected_conditions.presence_of_all_elements_located((selector, selection))
    return all_elements_present

def presenceLocated(selector, selection):
    presence_located = expected_conditions.presence_of_element_located((selector, selection))
    return presence_located

def selectByVisibleID(driver, id):
    drop_down = Select(waitUntil(driver, visible, By.ID, id))
    return drop_down

def selectByClickableID(driver, id):
    drop_down = Select(waitUntil(driver, clickable, By.ID, id))
    return drop_down

def makeSelection(driver, dropdown, selection):
    dropdown.select_by_value(selection)
    return driver

def handleAuditor(driver, name="Jimbos Robot"):
    overlay = visibleXpath(driver, "//*[@id='user']")
    overlay.send_keys(name)
    submit = clickableXpath(driver, "//*[@id='form--di-audit-log-name']/div/div[2]/div/fieldset/div[2]/input")
    submit.click()
    time.sleep(2)
    return driver

def auditorCheck(driver):
    auditor_overlay = driver.find_elements_by_xpath("//*[@id='user']")
    if len(auditor_overlay) > 0:
        driver = handleAuditor(driver)
    return driver

def getTagFromUl(ul_element, tag_name):
    list_of_elements = ul_element.find_elements_by_tag_name(tag_name)
    return list_of_elements

def getTagAttribute(tag, attribute):
    attr = tag.get_attribute(attribute)
    return attr
