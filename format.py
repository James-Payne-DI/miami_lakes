import bs4, html2text, download, upload, config
from markdown2 import Markdown

# def content(raw_content, devsite):
#     count = 0
#     print(type(raw_content))
#     for content in raw_content:
#         if content.find('img'):
#             print("Image Found " + str(count))
#             new_images = content.find_all('img')
#             for new_img in new_images:
#                 if new_img.get('alt') == None:
#                     try:
#                         img_title = str(new_img["title"])
#                         new_img["alt"] = img_title
#                     except:
#                         new_img["alt"] = config.dealership_name
#             raw_content[count] = changeSrc(content, devsite)
#             count += 1
#
#     clean_content = []
#     for content in raw_content:
#         #if content.has_attr('class') and 'credit' in content['class']:
#         #    continue
#         print(content)
#         clean_content.append(convert(content.prettify()))
#
#     #turns the clean content back from a list into a string
#     clean_content = listToString(clean_content)
#     print(clean_content)
#     return clean_content

def content(raw_content, devsite):
    count = 0
    for content in raw_content:
        if content.find('img'):
            raw_content[count] = changeSrc(content, devsite)
            count += 1

    clean_content = []
    for content in raw_content:
        content = remove_extra_title(content)
        content = remove_extra_categories(content)
        content = remove_extra_date(content)
        find_a_tags(content)
        # print("………………… In format.py › content() …………………")
        # print(content)
        clean_content.append(convert(content.prettify()))
    clean_content = listToString(clean_content)

    return clean_content

def listToString(list):
    new_string = ""
    return new_string.join(list)


def markdown(text):
    markdowner = Markdown()
    htmlout = markdowner.convert(text)

    return htmlout

def convert(raw_content):
    text_maker = html2text.HTML2Text()
    text_maker.images_as_html = True
    text_maker.ignore_links = True
    text_maker.body_width = 0
    text = text_maker.handle(raw_content)
    text = markdown(text)
    return text


def replaceWithTags(raw_content, name=config.dealership_name, city=config.dealership_city):
    text_maker = html2text.HTML2Text()
    text_maker.images_as_html = True
    text_maker.ignore_links = True
    text_maker.body_width = 0
    text = text_maker.handle(raw_content)
    new_content = text.replace(str(name), '%%di_name%%')
    new_content = new_content.replace(str(city), '[di_dealer_option city=""]')
    #print(new_content)
    #new_content = new_content.replace(str(state), '[di_dealer_option state=""]')
    #print('Number of occurrence of each: ')
    #print('name: ', content.count(str(name)))
    #print('city: ', content.count(str(city)))
    #print('state: ', content.count(str(state)))
    return new_content



def changeSrc(content, devsite):
    #print("--------format.changeSrc called--------")
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', 'jpeg', 'JPG']
    img_src_list = []
    for img in content.findAll('img'):
        if img.has_attr('data-src') and img['data-src'] is not None and img['data-src'].startswith('http'):
            #print("Image has data-src: ", img['data-src'])
            img_src_list.append(img['data-src'])
        elif img.has_attr('src') and img['src'] is not None and img['src'].startswith('http') and img['src'].rindex(".") in suffix_list:
            #print("Image has src: ", img['src'])
            img_src_list.append(img['src'])
        elif img.has_attr('src') and img['src'] is not None and img['src'].startswith('//pictures') and img['src'].rindex(".") in suffix_list:
            new_src = 'http:' + str(img['src'])
            if download.checkStatusCode(new_src):
                #print(new_src)
                img_src_list.append(new_src)
        elif img.has_attr('src') and img['src'] is not None:
            new_src = 'http:' + str(img['src'])
            if download.checkStatusCode(new_src):
                #print(new_src)
                img_src_list.append(new_src)
        else:
            print('changeSrc Loop 1: IMAGE SOURCE NOT LOCATED')
            print(str(img))
            return content

    new_links = download.images(img_src_list, devsite)


    try:
        if len(new_links):
            print(str(len(new_links)) + " Image Links on This Page!")
    except:
        print("No DI Image Links Created on this page!")
        return content

    # The below loop should adjust the image source to be the DI image
    new_links_count = len(new_links)
    link_index = 0
    for img in content.findAll('img'):
        try:
            print(new_links[link_index])
        except:
            print("ERROR IN SRC REPLACEMENT -- Link Index:" + str(link_index) + "new_links:" + str(img))
            return content
        if new_links == []:
            print('changeSrc Loop 2: EMPTY LIST')
            return content
        elif img.has_attr('src') and img['src'] is not None:
            #print(new_links[link_index])
            img['src'] = new_links[link_index]
            link_index += 1
        elif img.has_attr('data-src') and img['data-src'] is not None:
            #print(new_links[link_index])
            img['data-src'] = new_links[link_index]
            link_index += 1
        else:
            print("ERROR IN SRC REPLACEMENT -- Link Index:" + str(link_index) + "new_links:" + str(img))
            link_index += 1

    return content

def data(title, slug, content, meta):
    # print("In Format.py: " + str(meta))
    metaData = lambda metaText: [metaText]
    meta = metaData(meta)
    # print(type(meta))
    # print('-'*50)
    data = {#'date': 'date',
            #'parent': 'parent',
            'title': title,
            'slug': slug,
            #'password': 'password',
            'status': 'publish',
            'content': content,
            'author': '1',
            # 'meta': meta,
            #'template': 'page template',
            #'excerpt': 'excerpt',
            'format': 'standard'
            }
    return data

def blogData(title, slug, content, meta, date, tags, categories, devsite):
    # print(tags)
    # print(categories)
    # print('-'*50)
    categories = upload.categories(devsite, categories)
    tags = upload.tags(devsite, tags)
    # print(date)
    data = {'date': date,
            #'parent': 'parent',
            'title': title,
            'slug': slug,
            #'password': 'password',
            'status': 'publish',
            'content': content,
            'author': '1',
            #'meta': meta,
            #'template': 'page template',
            #'excerpt': 'excerpt',
            'format': 'standard',
            'tags': tags,
            'categories': categories
            }

    return data



def blogDate(date):
    date = date.replace(',', '')
    date = date.split(' ')
    year = date[2].strip()
    month = formatMonth(date[0]).strip()
    day = date[1].strip()

    if len(day) <= 1:
        day = '0' + day

    return year +'-'+ month +'-'+ day + 'T09:00:00'


def formatMonth(month):
    months = {
        "january": "01",
        "jan": "01",
        "febuary": "02",
        "febuary": "02",
        "march": "03",
        "march": "03",
        "april": "04",
        "april": "04",
        "may": "05",
        "june": "06",
        "jun": "06",
        "july": "07",
        "jul": "07",
        "august": "08",
        "aug": "08",
        "september": "09",
        "sep": "09",
        "october": "10",
        "oct": "10",
        "november": "11",
        "nov": "11",
        "december": "12",
        "dec": "12"
    }
    month = month.lower()

    return months.get(month, "01")

def check_category_black_list(category):
    #print("--------format.check_category_black_list called--------")
    banned_strings = ['No Comments »','Uncategorized']
    status = "CLEAN"
    for item in banned_strings:
        if str(category) == item:
            #Use below print statement to help locate undesireable Categories
            #print("[Located In miami_lakes/format.py > 'check_category_black_list'] \n››› Banned Category Encountered ----> " + item)
            status = "BANNED"

    return status

def remove_extra_title(soup):
    #remove extra <h1> tags if found
    title = soup.find('div', {'class': 'titleDiv'})
    h1_tag = title.h1
    h1_tag.decompose()
    return soup

def remove_extra_categories(soup):
    #remove extra <h1> tags if found
    categories = soup.find('p', {'class': 'postmetadata'})
    categories.decompose()
    return soup

def remove_extra_date(soup):
    #remove extra <p> tags with date in them
    date = soup.find('div', {'class': 'dateDiv'})
    date.decompose()
    return soup

def find_a_tags(soup):
    print("›››--------format.find_a_tags called--------")
    try:
        text_content = soup.find('div', {'class': 'blogContent'})
        link_list = soup.find_all('a')
        print(link_list)
    except:
        print("›››------- Issue Finding <a> Tags -------")

def find_iframes(soup):
    print("›››--------format.find_a_tags called--------")
    try:
        text_content = soup.find('div', {'class': 'blogContent'})
        link_list = soup.find_all('iframe')
        print(link_list)
    except:
        print("›››------- Issue Finding <a> Tags -------")
