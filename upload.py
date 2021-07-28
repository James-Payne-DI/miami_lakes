import requests, json, base64, jsonFunctions, download, sqlite3, config


user = config.DI_USER
#password = 'bFbj 5bmV lAI6 hK2y zDBI RO8z'

password = config.DI_PASSWORD
rest_point = 'wp-json/wp/v2'
authString = user + ':' + password

token = base64.b64encode(authString.encode())

def getPostHeaders():
    post_headers = {'Authorization': 'Basic ' + token.decode('utf-8'),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'XDEBUG_SESSION=PHPSTORM'
                }
    return post_headers

def getMediaHeaders(file_name):
    media_headers = {'Authorization': 'Basic ' + token.decode('utf-8'),
                'Content-Type': 'image/jpg',
                'Content-Disposition': 'attachment; filename=%s'% file_name,
                'Cache-Control': 'no-cache'
                }
    return media_headers



def getEndpoint(devsite, type):
    return devsite+rest_point+type

def page(devsite, data, images):
    pages_endpoint = getEndpoint(devsite, '/pages')
    media_endpoint = getEndpoint(devsite, '/media')
    #print(str(data))

    page_response = requests.post(pages_endpoint, headers=getPostHeaders(), data=data)
    #print(page_response.status_code)
    # if page_response.status_code != 201:
    #     print(page_response.content)
    page_response = page_response.json()
    page_id = jsonFunctions.getPostId(page_response)
    #print(page_id)

    if images is not None:
        for file in images:
            filename = download.getImageFileName(file)

            open_file = open(file, "rb")
            bin_file = open_file.read()
            open_file.close()

            media_response = requests.post(media_endpoint, headers=getMediaHeaders(filename), data=bin_file)
        download.deleteImgFolder()
    return page_id

def blog(devsite, data, images):
    blog_endpoint = getEndpoint(devsite, '/posts')
    media_endpoint = getEndpoint(devsite, '/media')

    blog_response = requests.post(blog_endpoint, headers=getPostHeaders(), data=data)
    print(blog_response.status_code)
    if blog_response.status_code != 201:
        print(blog_response.content)
    blog_response = blog_response.json()
    page_id = jsonFunctions.getPostId(blog_response)

    if images is not None:
        for file in images:
            filename = download.getImageFileName(file)

            open_file = open(file, "rb")
            bin_file = open_file.read()
            open_file.close()

            media_response = requests.post(media_endpoint, headers=getMediaHeaders(filename), data=bin_file)
        download.deleteImgFolder()

def categories(devsite, categories_list):
    categories_endpoint = getEndpoint(devsite, '/categories')
    new_categories = []
    for category in categories_list:
        data = {'name': category}
        response = requests.post(categories_endpoint, headers=getPostHeaders(), data=data)
        response = response.json()
        id = response.get('id')
        new_categories.append(id)

    return new_categories
