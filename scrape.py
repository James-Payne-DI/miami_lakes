import bs4, requests, sqlite3, re
from bs4 import BeautifulSoup
from datetime import datetime
import format, download, upload, config, statusReports
from statusReports import GLOBAL_STATUS_REPORT as GSP
from statusReports import specialPrint

def livePage(url, selectors, devsite, db):
    raw_html = requests.get(url)
    og_soup = makeSoup(raw_html.content)
    soup = og_soup
    title = getTitle(soup)
    #Creates an instance for this post in the GLOBAL_STATUS_REPORT
    GSP[url] = {'page_id':'','page_data':'','error_list':[],'image_file_paths':[],'og_image_links':[],'di_image_links':[]}
    slug = getSlug(url)
    content = getContent(soup, selectors, devsite, title)
    meta = getMeta(soup)
    data = format.data(title, slug, content, meta)

    #confirms if the directory exists
    if download.directoryCheck('images'):
        #retrieves the filepaths for the images that will be uploaded
        image_file_paths = download.getImageFilePaths()
        #adds List of image file paths to Global Status Report
        GSP[url]['image_file_paths'] = image_file_paths
    else:
        image_file_paths = None
        GSP[url]['image_file_paths'] = "No Image File Paths were downloaded for thie Page: " + slug

    #Uploads content & sets the page ID return value (integer) to the page_id variable
    page_id = upload.page(devsite, data, image_file_paths)
    GSP[url]['page_id'] = page_id
    GSP[url]['page_data'] = data

    page_endpoint =  str(devsite) + "wp-json/wp/v2/pages/" + str(page_id)
    print("Page ID: " + str(page_endpoint))

    #adds the data as a new row in the metaData table within metaHousing
    db.execute('''INSERT INTO metaData(pageID, pageTitle, slug, meta) VALUES(?,?,?,?)''', (page_id, title, slug, meta))

    #we  can make adjustments  to  the  table here as well if needed.
    # cursor = db.cursor()
    # cursor.close()

def liveBlog(url, selectors, devsite, db):
    raw_html = requests.get(url)
    og_soup = makeSoup(raw_html.text)
    soup = og_soup

    title = getTitle(soup)
    #Creates an instance for this post in the GLOBAL_STATUS_REPORT
    GSP[url] = {'page_id':'','page_data':'','error_list':[],'image_file_paths':[],'og_image_links':[],'di_image_links':[]}

    slug = getSlug(url)
    categories = getCategoryFromSlug(url)
    tags = getCategoriesAsTags(soup)
    # Get the date for the blog post
    date = getBlogDate(soup)
    meta = getMeta(soup)
    content = getContent(soup, selectors, devsite, title)


    # categories = getCategories(soup)
    data = format.blogData(title, slug, content, meta, date, tags, categories, devsite)
    #print(data)

    if download.directoryCheck('images'):
        #Downloads the images for this post and saves their paths to a variable as a list
        image_file_paths = download.getImageFilePaths()
        #adds List of image file paths to Global Status Report
        GSP[url]['image_file_paths'] = image_file_paths

    else:
        image_file_paths = None
        GSP[url]['image_file_paths'] = "No Image File Paths were downloaded for thie Post: " + slug

    post_id = upload.blog(devsite, data, image_file_paths)
    GSP[url]['post_id'] = post_id
    GSP[url]['post_data'] = data


    db.execute('''INSERT INTO metaData(pageID, pageTitle, slug, meta) VALUES(?,?,?,?)''', (post_id, title, slug, meta))



def makeSoup(html):
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def getTitle(soup):
    #code on line below is not the original version -- title = soup.find('h1') <-- OG
    # title = soup.find('h1', {'class': 'ddc-page-title'})
    try:
        title = soup.find('div', {'class': 'titleDiv'})
        title = title.h1.span.strong
    except:
        try:
            title = getTitleFromBreadcrumbs(soup)
            return title
        except:
            print("››› In 'getTitle' function ---> Couldin't find the <h1> tag...")
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
        title_string = format.remove_title_spacing(str(title.text))
        print("--» Post Title: " + title_string.strip())
        return title_string
    except:
        error_text = """
        ERROR 1.01: TITLE EXISTENCE IN QUESTION
        - Page Title is None after several attempts to find something that resembles a title, we have failed
        """
        print(error_text)
        return "Post Title Missing"

def getSlug(url):
    #Use This Try/Except statement to customize how you find the slug
    try:
        #This 'try' section is meant to be adjusted for each run
        slug = getSlugFromURL(url)
        return slug
    except:
        #If the custom 'try' section fails, this should work, however it will stack parent & child pages into one slug...
        #i.e. /blogs/news/whats-new-with-us/  ===> /blogs-news-whats-new-with-us/
        slug = url.split('.')[2]
        slug_index = slug.index('/')
        slug = slug[slug_index + 1:]
        print("--» Post Slug: " + slug)
        return slug


def getTitleFromSlug(url):
    #This splits the url into an array and sets the 3rd element in that array equal to the variable titled 'slug'
    slug = url.split('.')[2]
    slug = slug.replace('com/','')
    slug = slug.replace('/','')
    slug = slug.replace('-','')
    #we add one to the index number and take everything in the string from that point on and set it equal to 'slug'
    slug = slug.title()
    print("--» Post Slug: " + slug)
    return slug

def getTitleFromBreadcrumbs(soup):
    #print("--------- getTitleFromBreadcrumbs SOUP: ---------")
    post_title = soup.findAll('span', {'class': 'breadcrumbs-link'})[-1]

    post_title = post_title.text
    post_title = post_title.title()
    print("--» Post Title From Breadcrumbs: " + post_title)
    return post_title

def getBlogDate(soup):
    date_string = ""
    print("--------- getBlogDate(soup) ---------")
    try:
        date = soup.find('time', {'class': 'entry-date'})
        date_string = str(date['datetime'])
        date_string = date_string[:-6]
        date_string =  date_string
    except:
        try:
            specialPrint("TRYING BACKUP METHOD","scrape.py › getBlogDate(soup) » getBlogDate_backup(soup)")
            #if Errors out try to grab the text from the time tag
            date_string = getBlogDate_backup(soup)
        except:
            specialPrint("TRYING BACKUP METHOD","scrape.py › getBlogDate(soup) » getBlogDate_backup(soup)")
            #if Neither works, return today's date
            date_string = "2023-02-02-T09:00:00"
    finally:
        print("--» Post Date: " + date_string)
        return date_string

def getBlogDate_backup(soup):
    date_string = ""
    date = soup.findAll('div', {'class': 'entry-meta'})[0]
    time_tag = str(date.a.time.text)
    date_string = format.blogDate(time_tag)
    print("--» Post Date: " + date_string)
    return date_string


def getContent(soup, selectors, devsite, title):
    #can remove specific sections we don't want migrated and deletes them from the soup
    soup = saniSoup(soup)

    #Testing to see if we can find inventory on pages and replace them with shortcodes
    # inventory_check = inventoryCheck(soup)
    # if inventory_check:
    #     print(inventory_check)


    #gets any tables on the page and formats them as a string
    try:
        table_strings = getTables(soup)
        if table_strings != []:
            tables = soup.find_all('table')
            count = 0
            for table in tables:
                print(table_strings[count])
                soup.find('table').replace_with(table_strings[count])
                count += 1
    except:
        print("--»in 'getContent()': Issue trying to get the table data --- this broke the script")

    #Finds the Content that we do want i.e. ('div', {'class': selectors})
    print('--» Post Selectors: ' + selectors[0] + ' -- ' + selectors[1] + ' -- ' + selectors[2])
    raw_content = soup.findAll(selectors[0], {selectors[1]: selectors[2]})
    #print(raw_content)
    #makes the soup content nice and pretty.
    content = format.content(raw_content, devsite, title)
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
    classList = config.DECOMP_IDS

    #soup = remove_redundant_images(soup)
    #new_soup = removeRedundantImages(new_soup)

    for target in classList:
        for div in soup.findAll(target[0], {target[1]: target[2]}):
            div.decompose()
    return soup


def getTables(soup):
    full_list = []
    table_strings = []
    # Creating list with all tables
    tables = soup.find_all('table')
    for table in tables:
        # Collecting Ddata
        try:
            for row in table.tbody.find_all('tr'):
                # Find all data for each column
                columns = row.find_all('td')
                full_list.append(columns)

            table_string = ""
            if full_list == []:
                print("--» No Table Found")
                return full_list
            else:
                print("--» Table Found")
                table_string = formatTable(full_list)
                table_strings.append(table_string)
        except:
            print("--» Issue trying to get the table data --- this broke the script")
            continue

    return table_strings

def formatTable(table_list):
    for row in table_list:
        count = 0
        for cell in row:
            try:
                if cell == None:
                    print(cell)
                    row[count] = '<td></td>'
                elif cell.text:
                    print(cell.text)
                    newData = '<td style="border: 1px solid black;padding-left:3px">' +  str(cell.text) + '</td>'
                    row[count] = newData
                else:
                    newData = '<td style="border: 1px solid black;padding-left:3px">' +  str(cell.div.span.string) + '</td>'
                    row[count] = newData
                count += 1
            except:
                try:
                    if cell.b == None:
                        print(cell)
                        row[count] = '<td></td>'
                    elif cell.strong.span:
                        newData = '<td style="border: 1px solid black;padding-left:3px">' +  str(cell.strong.span.string) + '</td>'
                        row[count] = newData
                    else:
                        newData = '<td style="border: 1px solid black;padding-left:3px">' +  str(cell.div.span.string) + '</td>'
                        row[count] = newData
                    count += 1
                except:
                    print(cell)
                    row[count] = '<td></td>'

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

def getCategoriesAsTags(soup):
    # categories = soup.find('div', {'class': 'categories'})
    clean_categories = []
    error_message = "----- No Categories Found ----- "
    try:
        categories = soup.find('aside', {'id': 'categories-2'})
        if categories is None:
            print("››› In 'If/Else' Statement ---> " + error_message)
            return clean_categories
        else:
            for category in categories.findAll('li', {'class': 'cat-item'}):
                category = category.a.text
                category.strip()
                #Check the banned list of categories
                cat_check = format.check_category_black_list(category)
                #If the category string does not match any banned strings in the list...
                if cat_check == "CLEAN":
                    #« then it gets added to the 'clean_categories' array
                    clean_categories.append(category)
            return clean_categories
    except:
        specialPrint(error_message, 'getCategoriesAsTags › "except" Statement\n-->Categories NOT FOUND')
        return clean_categories

def getCategories(soup):
    # categories = soup.find('div', {'class': 'categories'})
    clean_categories = []
    error_message = "----- No Categories Found ----- "
    try:
        categories = soup.find('aside', {'id': 'categories-2'})
        if categories is None:
            print("››› In 'If/Else' Statement ---> " + error_message)
            return clean_categories
        else:
            for category in categories.findAll('li', {'class': 'cat-item'}):
                category = category.a.text
                category.strip()
                #Check the banned list of categories
                cat_check = format.check_category_black_list(category)
                #If the category string does not match any banned strings in the list...
                if cat_check == "CLEAN":
                    #« then it gets added to the 'clean_categories' array
                    clean_categories.append(category)
            return clean_categories
    except:
        #print("››› In 'Try/Except' Statement ---> " + error_message)
        specialPrint(error_message, 'getCategories › "except" Statement\n-->Categories NOT FOUND')
        return clean_categories

def removeLiveDomain(url, domain):
    url = str(url)
    if domain in url:
        slug = url.replace(domain, '')
        print('_♦_| Domain Removed')
        return slug
    else:
        return url

def checkSlugForParent(slug):
    try:
        new_slug = ''
        url_pieces = slug.split('/')
        new_slug = url_pieces[-2]
        print('_♦_| Slug Text extracted from parent')
        print(new_slug)
        return new_slug
    except:
        print('_♦_| FAILED to extract slug text')
        url_pieces = slug.split('/')
        specialPrint(url_pieces, 'scrape.py > checkSlugForParent()')
        return slug
def getSlugFromURL(postUrl):
    print("›››--------scrape.getSlugFromURL called--------")
    split_link = postUrl.split('/')
    if len(split_link) > 1:
        post_slug = str(split_link[-2])
        print("--» Post Slug: " + post_slug)
        return post_slug
    else:
        post_slug = str(split_link[0])
        print("--» Post Slug: " + post_slug)
        return post_slug


def remove_redundant_images(soup):
    try:
        div_tags = soup.findAll('div',{'class','widget-image'})
        for tag in div_tags:
            lower_div = tag.div
            img = tag.picture.img
            # if check_specific_case(img):
            #     pic.decompose()
            #     specialPrint("SUCCESS - Tag Decomposed prior to download", "scrape.py > remove_redundant_images()")
            #     continue
            if check_undesired_image_list(format.get_source_url(img)):
                lower_div.decompose()
                print(tag)
                specialPrint("SUCCESS - Tag Decomposed prior to download", "scrape.py > remove_redundant_images()")
            else:
                specialPrint("SUCCESS - Tag Intentionally skipped!", "scrape.py > remove_redundant_images()")
        return soup
    except:
        specialPrint("FAILURE - Tag not Decomposed prior to download :(", "scrape.py > remove_redundant_images()")
        return soup

def check_specific_case(img_tag):
    try:
        img_url = img_tag['src']
        is_found = re.search("Miami_Lakes_Logo[0-9]{1,4}\.jpeg", img_url)
        if is_found:
            print("Specific Case Found!")
            return True
        else:
            return False
    except:
        return False
def check_undesired_image_list(img_url):
    url = str(img_url)
    img_list = ["performance[0-9]{1,4}\.png$","exterior[0-9]{1,4}\.png$","technology[0-9]{1,4}\.png$","information[0-9]{1,4}\.png$", "Miami_Lakes_Logo[0-9]{1,4}\.jpeg"]
    for item in img_list:
        is_found = re.search(item, url)
        if is_found:
            print("Found!")
            return True
    return False


def getCategoryFromSlug(postUrl):
    cat_list = []
    split_link = postUrl.split('/')
    #specialPrint(split_link, 'getCategoryFromSlug')
    primary_category = str(split_link[-3])
    cat_list.append(primary_category)
    return cat_list
