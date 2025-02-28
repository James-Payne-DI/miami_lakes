import requests, json, base64, jsonFunctions, download, sqlite3, config, date, logging
from statusReports import specialPrint

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
    # meta_response = requests.get(post_endpoint)
    # meta_response = meta_response.json()
    # print(meta_response['meta'])

    # meta_response = requests.post(post_endpoint, headers=getPostHeaders(), data={'description':meta_desc})
    # meta_response = meta_response.json()
    # post_meta = meta_response.get('meta')
    # print(post_meta)

    return page_id

def blog(devsite, data, images):
    
    blog_endpoint = getEndpoint(devsite, '/posts')
    media_endpoint = getEndpoint(devsite, '/media')

    tag_list = data['tags']
    tag_list = csvList(tag_list)

    category_list = data['categories']
    category_list = csvList(category_list)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    blog_response = requests.post(blog_endpoint, headers=getPostHeaders(), data=data)
    print("--» Post Response Status Code: " + str(blog_response.status_code))
    if blog_response.status_code != 201:
        print("--» Post Response Content:")
        print(blog_response.content)
    blog_response = blog_response.json()
    post_id = jsonFunctions.getPostId(blog_response)


    post_endpoint = blog_endpoint + '/' + str(post_id)
    print("--» Post Endpoint: " + str(post_endpoint))


    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Trying to upload the Post Tags via REST
    post_tags = []
    try:
        tag_response = requests.post(post_endpoint, headers=getPostHeaders(), data={'tags':tag_list})
        tag_response = tag_response.json()
        post_tags = tag_response.get('tags')
        print("--» Post Tags: ", post_tags)
    except:
        if tag_list == []:
            print("_♦_|______________ALERT - NO TAGS Uploaded______________ ")
    else:
        print("_♦_|______________Tags added to Post______________")


    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Trying to upload the Post Categories via REST
    post_categories = []
    try:
        category_response = requests.post(post_endpoint, headers=getPostHeaders(), data={'categories':category_list})
        category_response = category_response.json()
        category = category_response.get('categories')
        print("--» Post Categories: ", category)
    except:
        print("_♦_|______________Category list not found - using 'Uncategorized' as category______________")
        post_categories = [1]
        category_response = requests.post(post_endpoint, headers=getPostHeaders(), data={'categories':post_categories})
        category_response = category_response.json()
        category = category_response.get('categories')
        print("--» Post Categories: ", category)
    else:
        print("_♦_|______________Category List added to Post______________")
    

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Uploading the Image(s) for this post
    print('_♦_|______________Uploading Images________________')
    
    # Declaring the 'media_id' variable and setting it equal to 'None'
    media_id = None
    if images is not None:
        for file in images:
            filename = download.getImageFileName(file)

            open_file = open(file, "rb")
            bin_file = open_file.read()
            open_file.close()

            media_response = requests.post(media_endpoint, headers=getMediaHeaders(filename), data=bin_file)
            
            try:
                media_response = media_response.json()
                media_id = str(media_response['id'])
                print("--» Image uploaded ---- ID:", str(media_id))
            except ValueError as e:  # This handles JSONDecodeError
                logging.error(f"Failed to parse JSON: {e}")
                logging.info(f"Response content: {media_response.text}")
                media_id = None
                print('_♦_|______________Failed to retrieve Media ID______________')
            except:
                print(media_response)
                media_id = None
                print('_♦_|______________Failed to retrieve Media ID______________')

            
            #Setting The Media ID to be used for the Featured Image
            #media_id = jsonFunctions.getPostId(media_response)
            
            
            #testImageLink(devsite, str(filename))
            
        download.deleteImgFolder()
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Trying to upload the featured Images via REST
    if media_id != None:
        try:
            #uploads the data
            featured_media_response = requests.post(post_endpoint, headers=getPostHeaders(), data={'featured_media':media_id})
            
            #checks for success of upload
            featured_media_response = featured_media_response.json()
            
            #checks the content we uploaded
            featured_media = featured_media_response.get('featured_media')
            print("--» Post Tags: ", featured_media)
        except:
            print("_♦_|______________ALERT - NO Feature Image Uploaded______________ ")
        else:
            print("_♦_|______________Feature Image added to Post______________")
    else:
        print("_♦_|______________ALERT - NO Feature Image Uploaded (missing 'media_id'______________ ")

    # End of Blog Post Uploads function
    return post_id


#__________________________________________________________________________________
#__________________________________________________________________________________
def categories(devsite, categories_list):
    categories_endpoint = getEndpoint(devsite, '/categories')
    new_categories = []
    for category in categories_list:
        data = {'name': category}
        response = requests.post(categories_endpoint, headers=getPostHeaders(), data=data)
        #print("***********" + 'Category' + "***********")
        response = response.json()
        #print(response)
        category_id = response.get('id')
        if category_id == None:
            elem = response.get('data')
            elem = elem['term_id']
            category_id = elem
        #print(id)
        new_categories.append(category_id)
    # print(new_categories)
    return new_categories



# def tags(devsite, tags_list):
# given a list of tags housed in the config.py file
#
# get the endpoint for the tags on this devsite
#
# if the list from the config file isn't empty
#     for each id in the list
#         check if there is an existing endpoint similar to this wp-json/wp/v2/tags/137
#         if it 404s then add that new tag



# def tags(devsite, tags_list):
#     print(tags_list)
#     tags_endpoint = getEndpoint(devsite, '/tags')
#     # new_tags = []
#     post_tags = []
#     tag_data = None
#     for tag in tags_list:
#         try:
#
#             data = {'name': tag}
#             tag_id = check_tagsAdded(data)
#             if tag_id:
#                 post_tags.append(tag_id)
#                 continue
#             response = requests.post(tags_endpoint, headers=getPostHeaders(), data=data)
#             #print("***********" + 'Tag ID' + "***********")
#             response = response.json()
#             specialPrint(response, "upload.py » tags(devsite tags_list) › response.json()")
#             id = response.get('id')
#             if id == None:
#                 elem = response.get('data')
#                 elem = elem['term_id']
#                 id = elem
#             data["tag_id"] = id
#             print(data)
#             post_tags.append(id)
#             add_to_tagsAdded(data)
#         except:
#             #specialPrint("FAILURE - adding new tag to devsite broke script", "upload.py » tags(devsite tags_list)")
#             continue
#         else:
#             print(str(id))
#             #specialPrint("SUCCESS - added new tag to devsite", "upload.py » tags(devsite tags_list)")
#     print(config.TAGS_ADDED_TO_DEVSITE)
#     return post_tags



def tags(devsite, post_tags):
    print(post_tags)
    upload_list = post_tags
    full_tag_list = []
    tags_endpoint = getEndpoint(devsite, '/tags')
    response = create_tagsAdded(tags_endpoint)
    for tag in response:
        tag_name = tag.get('name')
        tag_id = tag.get('id')
        if tag_name in post_tags:
            print(f"--» Tag Already Uploaded, adding the tag ID: {tag_id} to 'full_tag_list'")
            full_tag_list.append(tag_id)
            upload_list.remove(tag_name)
    print(f"Upload List: {upload_list}")
    for tag in upload_list:
        data = {'name': tag}
        response = requests.post(tags_endpoint, headers=getPostHeaders(), data=data)
        response = response.json()
        tag_id = response.get('id')
        if tag_id == None:
            elem = response.get('data')
            elem = elem['term_id']
            tag_id = elem
        full_tag_list.append(tag_id)

    return full_tag_list


def create_tagsAdded(tags_endpoint):
    all_tags_added = []
    # tags_endpoint = getEndpoint(devsite, '/tags')
    count = 1
    tags_found = True
    while count < 10:
        page_query = f"?per_page=100&page={str(count)}"
        print(page_query)
        tags_endpoint = tags_endpoint + page_query
        response = requests.get(tags_endpoint)
        try:
            response = response.json()
        except:
            print("--» response.json() ended the while loop")
            break
        if response == []:
            break
        all_tags_added = all_tags_added + response
        count += 1

    return all_tags_added

def add_to_tagsAdded(tag_data):
    if check_tagsAdded(tag_data):
        return tag_data
    else:
        print("--» Tag added to big list")
        config.TAGS_ADDED_TO_DEVSITE.append(tag_data)
        return False
def check_tagsAdded(tag_data):
    tags_added = config.TAGS_ADDED_TO_DEVSITE
    if tag_data in tags_added:
        return True
    else:
        return False

def testImageLink(devsite, filename):
    print("›››--------upload.testImageLink called--------")
    img_url = download.createDevLink(devsite, filename)
    if download.checkStatusCode(img_url):
        print("--» Image checked out")
    else:
        new_name = str(filename)
        new_name = new_name.replace(".jpg","-1.jpg")
        img_url = download.createDevLink(devsite, new_name)
        print(img_url)
        if download.checkStatusCode(img_url):
            print("--»  -1 theory SUCCESS!!!")
        else:
            print("--» -1 theory FAILURE :(")
def splitString(str, char):
    string_list = str.split(char)
    return string_list
def getImageLink(devsite, img_name):
    dev_link = "https://di-uploads-development.dealerinspire.com/" + splitString(splitString(devsite, '/')[2], '.')[0] + '/uploads/' + date.getYear() + '/' + date.getMonth() + '/' + img_name
    print("››› DI Image Link Created:\n" + str(dev_link))
    return dev_link
def csvList(list_item):
    converted_list = [str(element) for element in list_item]
    joined_string = ",".join(converted_list)
    return joined_string
