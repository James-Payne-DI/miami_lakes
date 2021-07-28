import bs4, html2text, download, upload
from markdown2 import Markdown

def content(raw_content, devsite):
    count = 0
    for content in raw_content:
        if content.find('img'):
            raw_content[count] = changeSrc(content, devsite)
            count += 1

    clean_content = []
    for content in raw_content:
        #if content.has_attr('class') and 'credit' in content['class']:
        #    continue
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
    text_maker.ignore_images = False
    text_maker.ignore_links = True
    text_maker.body_width = 0
    text = text_maker.handle(raw_content)
    text = markdown(text)
    return text


def changeSrc(content, devsite):
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', 'jpeg', 'JPG']
    img_src_list = []
    for img in content.findAll('img'):
        if img.has_attr('data-src') and img['data-src'] is not None and img['data-src'].startswith('http'):
            img_src_list.append(img['data-src'])
        elif img.has_attr('src') and img['src'] is not None and img['src'].startswith('http') and img['src'].rindex(".") in suffix_list:
            img_src_list.append(img['src'])
        else:
            return content

    new_links = download.images(img_src_list, devsite)
    link_index = 0
    for img in content.findAll('img'):
        #print(new_links[link_index])
        if img.has_attr('src') and img['src'] is not None:
            img['src'] = new_links[link_index]
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
    categories = upload.categories(devsite, categories)
    tags = upload.categories(devsite, tags)
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
