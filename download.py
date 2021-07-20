#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, os, shutil, re, date, time
from io import open as iopen

def images(url_list, devsite):
    if len(url_list) < 1:
        print('No Images found on the page')
        return
    dev_links = []
    for url in url_list:
        url = cleanUrl(url)
        suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', 'jpeg', 'JPG']
        file_suffix = splitString(url, '.')[-1]
        file_name = splitString(url, '/')[-1]

        image = None
        if file_suffix in suffix_list:
            image = requests.get(url)
            time.sleep(0.5)
        if image is not None and image.status_code == requests.codes.ok:
            if directoryCheck('images') == False:
                makeNewFolder('images')
            writeFile('images', file_name, image)
            dev_links.append(createDevLink(devsite, file_name))
        else:
            print('Could not download ' + url)
            print('Status code: ' + image.status_code)

    optomizeImages('images')

    return dev_links

def createDevLink(devsite, img_name):
    dev_link = "https://di-uploads-development.dealerinspire.com/" + splitString(splitString(devsite, '/')[2], '.')[0] + '/uploads/' + date.getYear() + '/' + date.getMonth() + '/' + img_name
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
    os.system('/Applications/ImageOptim.app/Contents/MacOS/ImageOptim ' + folder_name)

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

def createPath(folder_name, file_name):
    #current_folder = getCurrentFolder()
    return os.path.join(os.getcwd(), folder_name, file_name)

def writeFile(folder_name, file_name, request_object):
    file_path = createPath(folder_name, file_name)
    with open(file_path, 'wb') as file:
        file.write(request_object.content)
        file.close()
