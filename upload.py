import requests, json, base64, jsonFunctions, download, sqlite3, config

user = config.DI_USER
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
    print("page response: " + str(page_response.status_code))
    if page_response.status_code != 201:
        print(page_response.content)
    page_response = page_response.json()
    page_id = jsonFunctions.getPostId(page_response)
    print(page_id)

    if images is not None:
        for file in images:
            filename = download.getImageFileName(file)

            open_file = open(file, "rb")
            bin_file = open_file.read()
            open_file.close()

            media_response = requests.post(media_endpoint, headers=getMediaHeaders(filename), data=bin_file)
        download.deleteImgFolder()

    post_endpoint = pages_endpoint + '/' + str(page_id)
    # print(post_endpoint)
    #meta_desc = data["meta"]
    # print("In upload.py: " + str(meta_desc))
    # print('-'*50)
    meta_response = requests.get(post_endpoint)
    meta_response = meta_response.json()
    print(meta_response['meta'])

    # meta_response = requests.post(post_endpoint, headers=getPostHeaders(), data={'description':meta_desc})
    # meta_response = meta_response.json()
    # post_meta = meta_response.get('meta')
    # print(post_meta)

    return page_id

def blog(devsite, data, images):
    blog_endpoint = getEndpoint(devsite, '/posts')
    media_endpoint = getEndpoint(devsite, '/media')


    # print("***********" + 'Categories & Tags' + "***********")
    # print(data['tags'])
    # print(data['categories'])
    tag_list = data['tags']
    tag_list = csvList(tag_list)

    category_list = data['categories']
    category_list = csvList(category_list)


    blog_response = requests.post(blog_endpoint, headers=getPostHeaders(), data=data)
    print(blog_response.status_code)
    if blog_response.status_code != 201:
        print(blog_response.content)
    blog_response = blog_response.json()
    post_id = jsonFunctions.getPostId(blog_response)


    post_endpoint = blog_endpoint + '/' + str(post_id)
    print(post_endpoint)
    # for i in data['tags']:
    #     tag_response = requests.post(post_endpoint, headers=getPostHeaders(), data=data['tags'])
    #     tag_response = tag_response.json()
    #     tag = tag_response.get('tags')
    #     print(tag)
    #
    # for i in data['categories']:
    #     category_response = requests.post(post_endpoint, headers=getPostHeaders(), data=data['categories'])
    #     category_response = category_response.json()
    #     category = category_response.get('categories')
    #     print(category)


    tag_response = requests.post(post_endpoint, headers=getPostHeaders(), data={'tags':tag_list})
    tag_response = tag_response.json()
    tag = tag_response.get('tags')
    print(tag)

    category_response = requests.post(post_endpoint, headers=getPostHeaders(), data={'categories':category_list})
    category_response = category_response.json()
    category = category_response.get('categories')
    print(category)


    if images is not None:
        for file in images:
            filename = download.getImageFileName(file)

            open_file = open(file, "rb")
            bin_file = open_file.read()
            open_file.close()

            media_response = requests.post(media_endpoint, headers=getMediaHeaders(filename), data=bin_file)
        download.deleteImgFolder()

    return post_id

def categories(devsite, categories_list):
    categories_endpoint = getEndpoint(devsite, '/categories')
    new_categories = []
    for category in categories_list:
        data = {'name': category}
        response = requests.post(categories_endpoint, headers=getPostHeaders(), data=data)
        #print("***********" + 'Category' + "***********")
        response = response.json()
        #print(response)
        id = response.get('id')
        if id == None:
            elem = response.get('data')
            elem = elem['term_id']
            id = elem
        #print(id)
        new_categories.append(id)
    # print(new_categories)
    return new_categories

def tags(devsite, tags_list):
    tags_endpoint = getEndpoint(devsite, '/tags')
    new_tags = []
    for tag in tags_list:
        data = {'name': tag}
        response = requests.post(tags_endpoint, headers=getPostHeaders(), data=data)
        #print("***********" + 'Tag ID' + "***********")
        response = response.json()
        #print(response)
        id = response.get('id')
        if id == None:
            elem = response.get('data')
            elem = elem['term_id']
            id = elem
        #print(id)
        new_tags.append(id)
    # print(new_tags)
    return new_tags


def csvList(list_item):
    converted_list = [str(element) for element in list_item]
    joined_string = ",".join(converted_list)
    return joined_string
