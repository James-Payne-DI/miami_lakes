from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, config

#def addToHubsite(driver,hubsite,sitekey,token,tags,user="dealerinspire",pwd="awesome1234"):
#!!!!Tags field removed for now

def logInToDevsite(driver,devsite,user=config.DEVSITE_USERNAME,pwd=config.DEVSITE_PASSWORD,name="Jimbos Robot"):
    driver = webdriver.Chrome(str(driver))

    #Use .get to go directly to the broadcaster link on the Hubsite
    driver.get(devsite)
    time.sleep(0.2)

    try:
        #Log In
        #have driver enter Username
        elem = driver.find_element_by_id("user_login")
        elem.send_keys(user)

        #have driver enter password
        elem = driver.find_element_by_id("user_pass")
        elem.send_keys(pwd)

        #Click log in button.
        #WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Log in')]"))).click()
        driver.find_element_by_xpath("//*[@id='wp-submit']").click()
        time.sleep(.5)
    except:
        #Log In
        #have driver enter Username
        elem = driver.find_element_by_id("user_login")
        elem.send_keys(user)

        #have driver enter password
        elem = driver.find_element_by_id("user_pass")
        elem.send_keys(config.DEVSITE_PASSWORD_2)

        #Click log in button.
        #WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Log in')]"))).click()
        driver.find_element_by_xpath("//*[@id='wp-submit']").click()
        time.sleep(.5)

    #enter Developer name for DI auditor
    elm = driver.find_elements_by_xpath("//*[@id='user']")
    if len(elm) > 0:
        elem = driver.find_element_by_xpath("//*[@id='user']")
        elem.send_keys(name)
        elem = driver.find_element_by_xpath("//*[@id='form--di-audit-log-name']/div/div[2]/div/fieldset/div[2]/input")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(2)

    time.sleep(1)
    print("Devsite Entered")

    return driver

#Sanitizing Inputs
def url_to_wp_admin(url):
    urlError = "Error?? UNRECOGNIZED_ADDRESS - Please Insert the base URL for this website and try again"

##    print('url[-5:] == '  + str(url[-5:]) + '\n' + 'url[-12:] == '  + str(url[-12:]))
    if url[-12:] != "wp/wp-admin/" and url[-5:] != ".com/":
        print(urlError)
        return url
    elif url[-12:] != "wp/wp-admin/" and url[-5:] == ".com/":
        url = url + "wp/wp-admin/"
##        print(url)
        return str(url)
    elif url[-17:] == ".com/wp/wp-admin/":
##        print(url)
        return str(url)
    else:
        print(urlError)
        return None

def nav_DISlides(driver,devsite):
    di_slides_url = devsite.replace("admin.php?page=di-broadcast","edit.php?post_type=di_slide")
    elem = logInToDevsite(driver,devsite)
    elem.get(di_slides_url)
    time.sleep(2)
    return elem

def nav_DISliders(driver,devsite):
    di_sliders_url = devsite.replace("admin.php?page=di-broadcast","edit.php?post_type=di_slider")
    elem = logInToDevsite(driver,devsite)
    elem.get(di_sliders_url)
    time.sleep(2)
    return elem
