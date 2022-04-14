import bs4, html2text, download, upload, config
from markdown2 import Markdown

def content(raw_content, devsite):
    count = 0
    #print(type(raw_content)
    for content in raw_content:
        if content.find('img'):
            new_images = content.find_all('img')
            for new_img in new_images:
                if new_img.get('alt') == None:
                    try:
                        img_title = str(new_img["title"])
                        new_img["alt"] = img_title
                    except:
                        new_img["alt"] = config.dealership_name
            raw_content[count] = changeSrc(content, devsite)
            count += 1

    clean_content = []
    for content in raw_content:
        #if content.has_attr('class') and 'credit' in content['class']:
        #    continue
        clean_content.append(convert(content.prettify()))

    #turns the clean content back from a list into a string
    clean_content = listToString(clean_content)

    #swaps the dealership info (name,city) brought in by the config.py file with the corresponding DI Tags
    #clean_content = replaceWithTags(clean_content, config.dealership_name, config.dealership_city)


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
    print(new_content)
    #new_content = new_content.replace(str(state), '[di_dealer_option state=""]')
    #print('Number of occurrence of each: ')
    #print('name: ', content.count(str(name)))
    #print('city: ', content.count(str(city)))
    #print('state: ', content.count(str(state)))
    return new_content



def changeSrc(content, devsite):
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', 'jpeg', 'JPG']
    img_src_list = []
    for img in content.findAll('img'):
        if img.has_attr('data-src') and img['data-src'] is not None and img['data-src'].startswith('http'):
            print("Image has data-src: ", img['data-src'])
            img_src_list.append(img['data-src'])
        elif img.has_attr('src') and img['src'] is not None and img['src'].startswith('http') and img['src'].rindex(".") in suffix_list:
            print("Image has src: ", img['src'])
            img_src_list.append(img['src'])
        else:
            return content

    new_links = download.images(img_src_list, devsite)
    print(new_links)
    link_index = 0
    for img in content.findAll('img'):
        #print(img)
        if new_links == []:
            return content
        elif img.has_attr('src') and img['src'] is not None:
            img['src'] = new_links[link_index]
            link_index += 1
        elif img.has_attr('data-src') and img['data-src'] is not None:
            img['data-src'] = new_links[link_index]
            link_index += 1
    return content

def data(title, slug, content, meta):
    data = {#'date': 'date',
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
            'format': 'standard'
            }
    return data

def blogData(title, slug, content, meta, date, tags, categories, devsite):
    # print(tags)
    # print(categories)
    # print('-'*50)
    categories = upload.categories(devsite, categories)
    tags = upload.tags(devsite, tags)
    print(date)
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
    year = date[2]
    month = formatMonth(date[0])
    day = date[1]

    if len(day) <= 1:
        day = '0' + day

    return year +'-'+ month +'-'+ day + 'T09:00:00'


def formatMonth(month):
    months = {
        "january": "01",
        "febuary": "02",
        "march": "03",
        "april": "04",
        "may": "05",
        "june": "06",
        "july": "07",
        "august": "08",
        "september": "09",
        "october": "10",
        "november": "11",
        "december": "12"
    }
    month = month.lower()

    return months.get(month, "01")
