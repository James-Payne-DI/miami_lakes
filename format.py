import bs4, html2text
from markdown2 import Markdown
import download, upload, config
from statusReports import GLOBAL_STATUS_REPORT as GSP
from statusReports import specialPrint

def content(raw_content, devsite, title):
    count = 0
    for content in raw_content:
        if content.find('img'):
            new_images = content.find_all('img')
            #print(new_images)
            for image in new_images:
                try:
                    if image['alt'] == None:
                        print("››› alt attribute exists & is empty")
                        image['alt'] = replace_alt_text(image, title)
                except:
                    add_alt_attribute(image, title)


            raw_content[count] = changeSrc(content, devsite, title)
            count += 1

    # ---»»»»»»»»--- FLAG ----
    for content in raw_content:
        if content.find('img'):
            new_images = content.find_all('img')
            #specialPrint(new_images, 'format.content')
    # ---»»»»»»»»---

    clean_content = []
    for content in raw_content:
        #Customized Content Cleaning Functions
        remove_extra_title(content)
        remove_back_to_top_links(content)
        #Generic Content Cleaning Functions
        content = find_a_tags(content)
        content = find_iframes(content)
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
    text_maker.ignore_links = False
    text_maker.body_width = 0
    text = text_maker.handle(raw_content)
    text = markdown(text)
    return text

def changeSrc(content, devsite, title):
    #print("--------format.changeSrc called--------")
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', 'jpeg', 'JPG']
    img_src_list = []
    data_src_count = 0
    src_count = 0
    srcset_count = 0
    no_source_count = 0

    for img in content.findAll('img'):
        if img.has_attr('data-src') and img['data-src'] is not None and img['data-src'].startswith('https'):
            #specialPrint(img['data-src'], "format.changeSrc:\n--» data-src detected!")
            img_src_list.append(img['data-src'])
            data_src_count += 1

        elif img.has_attr('data-src') and img['data-src'] is not None and img['data-src'].startswith('//cdn-ds'):
                new_src = str(img['data-src'])
                new_src = "https:" + new_src
                if download.checkStatusCode(new_src):
                    img_src_list.append(new_src)
                    data_src_count += 1
                else:
                    no_source_count += 1

        elif img.has_attr('src') and img['src'] is not None and img['src'].startswith('https://cdn-ds.com'):
            src = str(img['src'])
            if download.checkStatusCode(src):
                img_src_list.append(src)
                src_count += 1
            else:
                no_source_count += 1


        elif img.has_attr('src') and img['src'] is not None and img['src'].startswith('http'):
            # ---»»»»»»»»--- Custom to miami lakes auto mall ---««««««««---
            #NOTE: Think of the below if statement as a customized whitelist for image databases.
            if img['src'].startswith(config.LIVE_SITE_URL) and img.has_attr('srcset'):
                #  Retrieves the first link in the srcset list we create using the string from img['src']
                new_src = str(img['srcset'].split()[0])
                img_src_list.append(new_src)
                srcset_count += 1
                specialPrint(new_src, "format.changeSrc > srcset elif statement")
            elif img['src'].startswith('http://www.wikimotiveblogs.com') and img.has_attr('srcset'):
                new_src = str(img['srcset'].split()[0])
                img_src_list.append(new_src)
                srcset_count += 1
                specialPrint(new_src, "format.changeSrc > srcset elif statement")
            else:
                # specialPrint("POTENTIAL 404\n_♦_| Adding the img['src'] with the Live Site Url - ","format.changeSrc")
                # img_src_list.append(img['src'])
                specialPrint("POTENTIAL 404\n_♦_| Potential broken image removed from the post content","format.changeSrc")
                no_source_count += 1
            # END---»»»»»»»»--- Custom to miami lakes auto mall ---««««««««---
        # elif img.has_attr('src') and img['src'] is not None and img['src'].startswith('//pictures') and img['src'].rindex(".") in suffix_list:
        #     new_src = 'http:' + str(img['src'])
        #     print(new_src)
        #     if download.checkStatusCode(new_src):
        #         print(new_src)
        #         img_src_list.append(new_src)

        # elif img.has_attr('src') and img['src'] is not None and img['src'].startswith('http') and img['src'].rindex(".") in suffix_list:
            #print("Image has src: ", img['src'])
            # img_src_list.append(img['src'])

        else:
            print('changeSrc Loop 1: IMAGE SOURCE NOT LOCATED')
            print(str(img))
            no_source_count += 1
            return content

    #image_source_score is used to track the sources we pull from when taking images
    image_source_score = "data_src: {0} images | src: {1} images | srcset: {2} images | No Source/Broken Found: {3} images"
    image_source_score = image_source_score.format(str(data_src_count), str(src_count), str(srcset_count), str(no_source_count))
    specialPrint(str(image_source_score),"format.chamgeScr > image_source_scores")

    new_links = download.images(img_src_list, devsite)

    #checks the length of 'new_links' array
    try:
        if len(new_links):
            #prints the amount of images on the page if the length is greater than 0
            print(str(len(new_links)) + " Image Links on This Page!")
    except:
        #if this fails, we will skip the 2nd loop by returning all content here.
        print("No DI Image Links Created on this page!")
        return content

    # The below loop should adjust the image source to be the DI image
    #new_links_count = len(new_links)
    link_index = 0
    #We ensure the lists match up by using the same search parameters as the previous for loop...
    #--> the same search parameters, return the same list, in the same order.
    for img in content.findAll('img'):
        try:
            specialPrint(new_links[link_index], "format.changeSrc:\n--» List validtion SUCCESSFUL!")
        except:
            img_error = "ERROR IN SRC REPLACEMENT -- Link Index:" + str(link_index) + "new_links:" + str(img)
            # GSP[title]['error_list'].append(img_error)
            return content
        if new_links == []:
            #print('changeSrc Loop 2: EMPTY LIST')
            return content
        elif img.has_attr('src') and img['src'] is not None:
            #print(img['src'])
            img['src'] = new_links[link_index]
            #print(img['src'])
            link_index += 1
        elif img.has_attr('data-src') and img['data-src'] is not None:
            #print(img['data-src'])
            img['data-src'] = new_links[link_index]
            #print(img['data-src'])
            link_index += 1
        else:
            img_error = "ERROR IN SRC REPLACEMENT -- Link Index:" + str(link_index) + "new_links:" + str(img)
            # GSP[title]['error_list'].append(img_error)
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
    banned_strings = ['No Comments »','Uncategorized',config.LIVE_SITE_URL,config.LIVE_SITE_DOMAIN]
    status = "CLEAN"
    for item in banned_strings:
        if str(category) == item:
            #Use below print statement to help locate undesireable Categories
            #print("[Located In miami_lakes/format.py > 'check_category_black_list'] \n››› Banned Category Encountered ----> " + item)
            status = "BANNED"

    return status

def remove_extra_title(soup):
    #remove extra <h1> tags if found
    title = soup.find('h1')
    title.decompose()
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

def remove_back_to_top_links(soup):
    specialPrint('Trying to remove the "Back to top" <a> tags', 'format.remove_back_to_top_links')
    tags = soup.findAll('a', {'class': 'js-external-link'})
    for tag in tags:
        if str(tag.text) == "back to top":
            tag.decompose()
        else:
            continue
    return soup

def find_a_tags(soup):
    print("›››--------format.find_a_tags called--------")
    try:
        text_content = soup.find('div', {'class': 'blogContent'})
        link_list = soup.find_all('a')
        for link in link_list:
            url = str(link['href'])
            href_string = remove_internal_domain(url)
            link['href'] = href_string
        return soup
    except:
        print("›››------- No <a> Elements located -------")
        # GSP[title]['error_list'].append("Issue Finding <a> Tags: " + title)
        return soup

def find_iframes(soup):
    print("›››--------format.find_iframes called--------")
    raw_soup = soup
    try:
        text_content = soup.find('div', {'class': 'blogContent'})
        iframe_list = soup.find_all('iframe')
        counter = 0
        for iframe in iframe_list:
            parent = iframe.parent
            iframe_string = format_iframe(iframe)
            iframe.decompose()
            parent.string = iframe_string
        return soup
    except:
        print("›››------- No <iframe> Elements located-------")
        # GSP[title]['error_list'].append("››› Issue Finding <iframe> Tags: " + title)
        return raw_soup

def remove_title_spacing(title):
    title_string = title.strip()
    title_string = title_string.replace('\t','')
    title_string = title_string.replace('\n','')
    return title_string


#Checks if the domain for the url is the same as the one for the site we are migrating from
def remove_internal_domain(url):
    domain = "https://www." + config.LIVE_SITE_DOMAIN + ".com"
    #if it is the same, if deletes it and returns just the slug
    if domain in url:
        slug = url.replace(domain, '')
        slug = audit_href_slug(slug)
        return slug
    else:
        #else, it regurgitates the original url
        return url

def audit_href_slug(url):
    #splits
    if "." in url:
        elems = url.split('.')
        elem = str(elems[0]) + '/'
        return elem
    else:
        #else, it regurgitates the original slug
        return url


def replace_alt_text(new_img, title):
    try:
        new_alt_text = title + '_' + config.dealership_name
        return new_alt_text
    except:
        return config.dealership_name

def add_alt_attribute(new_img, title):
    print("›››--------format.add_alt_attribute called--------")
    new_img['alt'] = title + '_' + config.dealership_name
    return new_img

def format_iframe(soup):
    iframe = soup
    iframe_shell = ""
    if 'youtube' in str(iframe['src']):
        print("››› Youtube Video Found")
        youtube_shell = """
        <div class="embed-responsive embed-responsive-16by9"><iframe class="embed-responsive-item" src="{0}"></iframe></div>
        <div class="text-left">Is the tool above not loading on the page? <a href="{0}" target="_blank">Click Here to open it in a new tab <i class="fa fa-chevron-right" aria-hidden="true"></i></a></div>
        <br/><br/>
        """
        youtube_shell = youtube_shell.format(iframe['src'])
        iframe_shell = youtube_shell
    else:
        generic_shell = """
        <div class="text-center main-iframe"><iframe src="{0}" frameborder="0" scrolling="auto" width="100%" height="{1}"></iframe></div>
        <div class="text-left">Is the tool above not loading on the page? <a href="{0}" target="_blank">Click Here to open it in a new tab <i class="fa fa-chevron-right" aria-hidden="true"></i></a></div>
        <br/><br/>"""
        generic_shell = generic_shell.format(iframe['src'],iframe['height'])
        iframe_shell = generic_shell
    return iframe_shell
