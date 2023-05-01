#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, os, subprocess, shutil, re, time, wget
from io import open as iopen
import date
from statusReports import GLOBAL_STATUS_REPORT as GSP
from statusReports import specialPrint

def images(url_list, devsite):
    if len(url_list) < 1:
        print('››› No Images found on the page')
        return
    dev_links = []


    # if len(url_list) > 4:
    #     url_list.pop()
    #     print("››› removed logo image from the following list using 'url_list.pop()'...")
    #     specialPrint(url_list, 'download.py > images(url_list, devsite)')

    for url in url_list:
        url = cleanUrl(url)
        suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', 'jpeg', 'JPG']
        file_suffix = splitString(url, '.')[-1]
        file_name = splitString(url, '/')[-1]
        print("file_name: " + file_name  + " | " +  "file_suffix: " + file_suffix)

        image = None
        if file_suffix in suffix_list:
            image = requests.get(url, stream = True)
            time.sleep(0.5)
        #image = checkStatusCode(image)

        if image is not None and image.status_code == requests.codes.ok:
            if directoryCheck('images') == False:
                makeNewFolder('images')
            writeFile('images', file_name, image)
            dev_links.append(createDevLink(devsite, file_name))
        elif image is not None:
            if directoryCheck('images') == False:
                makeNewFolder('images')
            writeWithWget('images', url)
            dev_links.append(createDevLink(devsite, file_name))
            #print(dev_links)
        else:
            print(str(image.status_code) + ' Could not download: ' + url)

    if directoryCheck('images') == True:
        optomizeImages('images')

    return dev_links

def createDevLink(devsite, img_name):
    dev_link = "https://di-uploads-development.dealerinspire.com/" + splitString(splitString(devsite, '/')[2], '.')[0] + '/uploads/' + date.getYear() + '/' + date.getMonth() + '/' + img_name
    #print("››› DI Image Link Created:\n" + str(dev_link))
    return dev_link

def cleanUrl(url):
    try:
        pos = url.index("?")
        url = url[:pos]
    except ValueError:
        pass
    finally:
        return url

def getImageFilePaths():
    listOfImageNames = []
    for image in os.listdir('images'):
        listOfImageNames.append(os.path.join(os.getcwd(), 'images', image))

    return listOfImageNames

def getImageFilePath(file_name):
    for image in os.listdir('images'):
        if image.startswith(file_name):
            return os.path.join(os.getcwd(), 'images', image)

def deleteImgFolder():
    shutil.rmtree(os.path.join(os.getcwd(), 'images'))

def getImageFileName(file_path):
    file_name = os.path.basename(file_path)
    return file_name

def optomizeImages(folder_name):
    #sets the path name for the image folder
    path_name = '/Applications/ImageOptim.app/Contents/MacOS/ImageOptim ' + folder_name
    #optimizes the images with "os.system(path_name)" and keeps the output in the variable assigned with the outer argument

    # Define command and options wanted
    command = "/Applications/ImageOptim.app/Contents/MacOS/ImageOptim"
    # Ask user for file name(s) - SECURITY RISK: susceptible to shell injection
    filename = 'images'
    path = [command, filename]

    try:
        print("Trying to Capture the image data")
        result = subprocess.run(path, capture_output=True)
    except:
        print("Subprocess failed")
        os.system(path_name)

def splitString(str, char):
    string_list = str.split(char)
    return string_list

def directoryCheck(folder_name):
    #print(os.path.isdir(folder_name))
    return os.path.isdir(folder_name)

def makeNewFolder(folder_name):
    os.mkdir(folder_name)

def getCurrentFolder():
    return os.getcwd

def checkStatusCode(img_url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'}
        if requests.get(img_url, headers=headers).status_code == 200:
            print("››› Image URL Get Request Successful!")
            return img_url
    except:
        print("››› Image URL Get Request Failed!")
        return None

def createPath(folder_name, file_name):
    #current_folder = getCurrentFolder()
    return os.path.join(os.getcwd(), folder_name, file_name)

def writeFile(folder_name, file_name, request_object):
    file_path = createPath(folder_name, file_name)
    with open(file_path, 'wb') as file:
        file.write(request_object.content)
        file.close()

def testImageDownload(image_url):
    image = requests.get(image_url, stream = True)
    file_name = splitString(image_url, '/')[-1]
    makeNewFolder('test-images')
    writeFile('test-images', file_name, image)
    print("››› Image Downloaded")

def bar_custom(current, total, width=80):
    print("Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total))

def writeWithWget(folder_name, image_url):
    # Use wget download method to download specified image url.
    folder_path = os.path.join(os.getcwd(), folder_name)
    image_filename = wget.download(image_url, folder_path, bar=bar_custom)
