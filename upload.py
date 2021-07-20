import requests, json, base64, jsonFunctions, download

user = 'di_dashboard'
#password = 'bFbj 5bmV lAI6 hK2y zDBI RO8z'
#Live Sites ^
password = 'j6Dt A7fB sBEl elgz FEmc i7cw'
rest_point = 'wp-json/wp/v2'
authString = user + ':' + password

token = base64.b64encode(authString.encode())

def getPostHeaders():
    post_headers = {'Authorization': 'Basic ' + token.decode('utf-8'),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'XDEBUG_SESSION=PHPSTORM'
                }
    #print(post_headers)
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
    #print("pages_endpoint: " + str(pages_endpoint))
    #print("media_endpoint: " + str(media_endpoint))

    page_response = requests.post(pages_endpoint, headers=getPostHeaders(), data=data)
    print(page_response.status_code)

    page_response = page_response.json()
    #print(str(page_response))
    page_id = jsonFunctions.getPostId(page_response)
    #print(str(page_id))

    if images is not None:
        for file in images:
            filename = download.getImageFileName(file)

            open_file = open(file, "rb")
            bin_file = open_file.read()
            open_file.close()

            media_response = requests.post(media_endpoint, headers=getMediaHeaders(filename), data=bin_file)
        download.deleteImgFolder()


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
