import bs4, requests, format, download, upload, sqlite3, config
from bs4 import BeautifulSoup
from datetime import datetime

def livePage(url, selectors, devsite, db):
    raw_html = requests.get(url)
    soup = makeSoup(raw_html.content)
    title = getTitle(soup)
    slug = getSlug(url)
    content = getContent(soup, selectors, devsite)
    meta = getMeta(soup)
    data = format.data(title, slug, content, meta)

    if download.directoryCheck('images'):
        image_file_paths = download.getImageFilePaths()
    else:
        image_file_paths = None
    #print(data)
    #Uploads content & sets the page ID return value (integer) to the page_id variable
    page_id = upload.page(devsite, data, image_file_paths)
    print("Page ID: " + str(page_id))

    #adds the data as a new row in the metaData table within metaHousing
    db.execute('''INSERT INTO metaData(pageID, pageTitle, slug, meta) VALUES(?,?,?,?)''', (page_id, title, slug, meta))

    #we  can make adjustments  to  the  table here as well if needed.
    # cursor = db.cursor()
    # cursor.close()


    #old code --------
    #cursor.execute("SELECT * FROM metaData")
    #print(title + ' | ' + slug + ' | ' + meta)
    #upload.page(devsite, data, image_file_paths)

def liveBlog(url, selectors, devsite, db, url_date):
    raw_html = requests.get(url)
    soup = makeSoup(raw_html.text)
    #print(raw_html.text)
    title = getTitle(soup)
    slug = getSlug(url)
    content = getContent(soup, selectors, devsite)
    meta = getMeta(soup)
    #date = getDate(soup)
    date = url_date
    tags = getTags(soup)
    categories = getCategories(soup)
    data = format.blogData(title, slug, content, meta, date, tags, categories, devsite)
    # print(data['tags'])
    # print(data['categories'])
    if download.directoryCheck('images'):
        image_file_paths = download.getImageFilePaths()
    else:
        image_file_paths = None

    # print("Tags")
    # print(tags)
    # print("Categories")
    # print(categories)
    print(date)
    post_id = upload.blog(devsite, data, image_file_paths)

    db.execute('''INSERT INTO metaData(pageID, pageTitle, slug, meta) VALUES(?,?,?,?)''', (post_id, title, slug, meta))



def makeSoup(html):
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def getTitle(soup):
    #code on line below is not the original version -- title = soup.find('h1') <-- OG
    title = soup.find('h1', {'class': 'ddc-page-title'})
    print(title)
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
    try:
        return title.text
    except:
        error_text = """
        ERROR 1.01: TITLE EXISTENCE IN QUESTION
        - Page Title is None after several attempts to find something that resembles a title, we have failed
        """
        print(error_text)
        return error_text

def getSlug(url):
    slug = url.split('.')[2]
    slug_index = slug.index('/')
    slug = slug[slug_index + 1:]
    print(slug)
    return slug

def getContent(soup, selectors, devsite):
    #can remove specific sections we don't want migrated and deletes them from the soup
    soup = saniSoup(soup)

    #gets any tables on the page and formats them as a string
    table_string = getTables(soup)
    print(table_string)
    if table_string != []:
        soup.find('table').replace_with(table_string)


    #Finds the Content that we do want i.e. ('div', {'class': selectors})
    print('Selectors: ' + selectors[0] + ' -- ' + selectors[1] + ' -- ' + selectors[2])
    raw_content = soup.findAll(selectors[0], {selectors[1]: selectors[2]})

    #makes the soup content nice and pretty.
    content = format.content(raw_content, devsite)
    #print(content)
    return content


def getMeta(soup):
    meta = soup.find('meta', {'name': 'description'})
    if meta is None:
        backup = getTitle(soup)
        backup = " | " + str(backup)
        print("No Meta found, using backup!: " + str(backup))
        return str(backup)
    if str(meta.text) == "":
        raw_meta = str(meta).replace('<meta content="','')
        raw_meta = str(raw_meta).replace('" name="description"/>','')
        #print("raw_meta used: " + str(raw_meta))
        return raw_meta
    else:
        print("meta.text used")
        return meta.text

def saniSoup(soup):
    #classList = ["contact1","map1","hours1","contact2","mobileHero","contact-form","form-wrapper","mod-department-hours"]
    #classList = ["abg-dynamic-content service-make-model-year"]
    #Below is Norm Reeves:
    classList = config.DECOMP_IDS

    for target in classList:
        for div in soup.findAll(target[0], {target[1]: target[2]}):
            div.decompose()
    return soup

# def getTables(soup):
#     full_list = []
#     # Creating list with all tables
#     tables = soup.find_all('table')
#     for table in tables:
#         # Collecting Ddata
#         for row in table.tbody.find_all('tr'):
#             # Find all data for each column
#             columns = row.find_all('td')
#             full_list.append(columns)
#
#     if full_list == []:
#         print("No Table Found")
#         return full_list
#     else:
#         formatTable(full_list)
#     print(full_list)
#     return full_list

def getTables(soup):
    full_list = []
    # Creating list with all tables
    tables = soup.find_all('table')
    for table in tables:
        # Collecting Ddata
        for row in table.tbody.find_all('tr'):
            # Find all data for each column
            columns = row.find_all('td')
            full_list.append(columns)

    table_string = ""
    if full_list == []:
        #print("No Table Found")
        return full_list
    else:
        print("Table Found")
        table_string = formatTable(full_list)

    return table_string

def formatTable(table_list):
    for row in table_list:
        count = 0
        for cell in row:
            if cell.p == None:
                row[count] = '<td></td>'
            else:
                newData = '<td style="border: 1px solid black;padding-left:3px">' +  str(cell.p.string) + '</td>'
                row[count] = newData
            count  += 1

        row.insert(0,'<tr style="display=flex;">')
        row.append("</tr>")
    table_list.insert(0,['<tbody>'])
    table_list.append(["</tbody>"])
    table_list.insert(0,['<table style="width=100%;">'])
    table_list.append(["</table>"])

    table_string = ""
    for tag in table_list:
        new_string = ''.join(tag)
        table_string = table_string + new_string

    #print(table_string)
    return table_string

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
