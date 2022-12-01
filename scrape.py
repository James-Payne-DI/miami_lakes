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

    #Uploads content & sets the page ID return value (integer) to the page_id variable
    page_id = upload.page(devsite, data, image_file_paths)
    # print("Page ID: " + str(page_id))
    page_endpoint =  str(devsite) + "wp-json/wp/v2/pages/" + str(page_id)
    print("Page ID: " + str(page_endpoint))

    #adds the data as a new row in the metaData table within metaHousing
    db.execute('''INSERT INTO metaData(pageID, pageTitle, slug, meta) VALUES(?,?,?,?)''', (page_id, title, slug, meta))

    #we  can make adjustments  to  the  table here as well if needed.
    # cursor = db.cursor()
    # cursor.close()

def liveBlog(url, selectors, devsite, db):
    raw_html = requests.get(url)
    soup = makeSoup(raw_html.text)
    title = getTitle(soup)
    slug = getSlug(url)
    categories = getCategories(soup)
    tags = getTags(soup)
    # Get the date for the blog post
    date = getBlogDate(soup)
    meta = getMeta(soup)
    content = getContent(soup, selectors, devsite)


    # categories = getCategories(soup)
    data = format.blogData(title, slug, content, meta, date, tags, categories, devsite)
    #print(data)

    if download.directoryCheck('images'):
        image_file_paths = download.getImageFilePaths()
    else:
        image_file_paths = None

    post_id = upload.blog(devsite, data, image_file_paths)

    db.execute('''INSERT INTO metaData(pageID, pageTitle, slug, meta) VALUES(?,?,?,?)''', (post_id, title, slug, meta))



def makeSoup(html):
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def getTitle(soup):
    #code on line below is not the original version -- title = soup.find('h1') <-- OG
    # title = soup.find('h1', {'class': 'ddc-page-title'})
    title = soup.find('div', {'class': 'titleDiv'})
    title = title.h1.a
    #print(title)
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
        test_title = title.text
        print("--» Post Title: " + test_title.strip())
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
    print("Post Slug: " + slug)
    return slug

def getBlogDate(soup):
    #print("--------- getBlogDate SOUP: ---------")
    date = soup.find('div', {'class': 'dateDiv'})

    date = date.text
    date = format.blogDate(date)
    print("--» Post Date: " + date)
    return date

def getContent(soup, selectors, devsite):
    #can remove specific sections we don't want migrated and deletes them from the soup
    soup = saniSoup(soup)

    #Testing to see if we can find inventory on pages and replace them with shortcodes
    # inventory_check = inventoryCheck(soup)
    # if inventory_check:
    #     print(inventory_check)


    #gets any tables on the page and formats them as a string
    # table_string = getTables(soup)
    # print(table_string)
    # if table_string != []:
    #     soup.find('table').replace_with(table_string)


    #Finds the Content that we do want i.e. ('div', {'class': selectors})
    print('--» Post Selectors: ' + selectors[0] + ' -- ' + selectors[1] + ' -- ' + selectors[2])
    raw_content = soup.findAll(selectors[0], {selectors[1]: selectors[2]})
    #print(raw_content)
    #makes the soup content nice and pretty.
    content = format.content(raw_content, devsite)
    #print(content)
    return content

#Created while looking at a DealerOn site - please adjust classes for testing
def inventoryCheck(soup):
    test_string = '[inventory_lightning type="New,CTP" make="Chevrolet" strict="type" /]'
    try:
        inventory_container = soup.find('div', {'id': 'content-main-inventory'})
        return test_string
    except:
        print("Inventory Container Not Detected!")
        return None

def getMeta(soup):
    meta = soup.find('meta', {'name': 'description'})
    if meta is None:
        backup = getTitle(soup)
        backup = " | " + str(backup)
        # print("No Meta found, using backup!: " + str(backup))
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
    # categories = soup.find('div', {'class': 'categories'})
    clean_categories = []
    error_message = "----- No Categories Found ----- "
    try:
        categories = soup.find('p', {'class': 'postmetadata'})
        if categories is None:
            print("In 'If/Else' Statement ---> " + error_message)
            return clean_categories
        else:
            for category in categories.findAll('a'):
                category = category.text
                category.strip()
                #Check the banned list of categories
                cat_check = format.check_category_black_list(category)
                #If the category string does not match any banned strings in the list...
                if cat_check == "CLEAN":
                    #« then it gets added to the 'clean_categories' array
                    clean_categories.append(category)
            return clean_categories
    except:
        print("In 'Try/Except' Statement ---> " + error_message)
        return clean_categories
