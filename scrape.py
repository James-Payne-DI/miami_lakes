import bs4, requests, format, download, upload
from bs4 import BeautifulSoup
from datetime import datetime

def livePage(url, selectors, devsite):
    raw_html = requests.get(url)
    soup = makeSoup(raw_html.content)
    title = getTitle(soup)
    slug = getSlug(url)
    content = getContent(soup, selectors, devsite)
    meta = getMeta(soup)
    data = format.data(title, slug, content, meta)
    #print(data)
    if download.directoryCheck('images'):
        image_file_paths = download.getImageFilePaths()
    else:
        image_file_paths = None
    #print(data['title'])
    #print(data['content'])
    #print(data['slug'])
    upload.page(devsite, data, image_file_paths)

def liveBlog(url, selectors, devsite):
    raw_html = requests.get(url)
    soup = makeSoup(raw_html.text)
    #print(raw_html.text)
    title = getTitle(soup)
    slug = getSlug(url)
    print(url)
    content = getContent(soup, selectors, devsite)
    meta = getMeta(soup)
    date = getDate(soup)
    tags = getTags(soup)
    categories = getCategories(soup)
    data = format.blogData(title, slug, content, meta, date, tags, categories, devsite)
    if download.directoryCheck('images'):
        image_file_paths = download.getImageFilePaths()
    else:
        image_file_paths = None

    upload.blog(devsite, data, image_file_paths)



def makeSoup(html):
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def getTitle(soup):
    title = soup.find('h1')
    if title is None:
        title = soup.find('strong', {'role': 'heading'})
        if title is None:
            title = soup.find('title')
            if title is None:
                count = 1
                while title is None:
                    if count > 6:
                        title = "No Title Found"
                    else:
                        heading = 'h'+str(count)
                        title = soup.find(heading)
                        count += 1
    return title.text

def getSlug(url):
    slug = url.split('.')[2]
    slug_index = slug.index('/')
    slug = slug[slug_index + 1:]
    return slug

def getContent(soup, selectors, devsite):
    soup = saniSoup(soup)
    raw_content = soup.findAll('div', {'data-widget-id': selectors})
    #print(raw_content)
    content = format.content(raw_content, devsite)
    return content


def getMeta(soup):
    meta = soup.find('meta', {'name': 'description'})
    if meta is None:
        return 1
    if str(meta.text) == "":
        raw_meta = str(meta).replace('<meta content="','')
        raw_meta = str(raw_meta).replace('" name="description"/>','')
        print("raw_meta used: " + str(raw_meta))
        return raw_meta
    else:
        print("meta.text used")
        return meta.text

def saniSoup(soup):
    for div in soup.findAll("div", {'data-widget-id': 'contact1'}):
        div.decompose()
    return soup

def getDate(soup):
    date = soup.find('time')
    if date is not None:
        blog_date = date['datetime'] + 'T09:00:00'
        return blog_date
    else:
        date = datetime.today()
        date = date.isoformat()
        date = date.split('.')[0]
        return date

def getTags(soup):
    tags = soup.find('div', {'class':'tags'})
    clean_tags =  []
    if tags is None:
        return clean_tags

    for a in tags.findAll('a'):
        clean_tags.append(a.text)

    return clean_tags

def getCategories(soup):
    categories = soup.find('div', {'class': 'categories'})
    clean_categories = []
    if categories is None:
        return clean_categories


    for category in categories.findAll('a'):
        clean_categories.append(category.text)

    return clean_categories
