import bs4, html2text, re
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
                        image['alt'] = replace_alt_text(title)
                except:
                    add_alt_attribute(image, title)
                    specialPrint(str(image['alt']), "format.py > content() » add_alt_attribute(image, title)")


            raw_content[count] = changeSrc(content, devsite, title)
            count += 1

    # ---»»»»»»»»--- FLAG ----
    # for content in raw_content:
    #     if content.find('img'):
    #         new_images = content.find_all('img')

            #specialPrint(new_images, 'format.content')
    # ---»»»»»»»»---

    clean_content = []
    #specialPrint(raw_content, "format.py > content() » Before thr Loop 'for content in raw_content:' » content")
    for content in raw_content:
        #Customized Content Cleaning Functions
        #---------Non-Specific---------
        content = remove_extra_title(content)

        #---------Specific For Blog Posts---------
        content = remove_duplicate_image(content)

        #---------Specific For pages---------
        #content = remove_back_to_top_links(content)
        #content = remove_picture_tag(content)
        #content = replace_consistent_images(content)

        #Generic Content Cleaning Functions
        content = find_a_tags(content)
        content = find_iframes(content)
        #content = find_table_tags(content)

        # print("………………… In format.py › content() …………………")
        # print(content)
        #specialPrint(convert(content.prettify()), "format.py > content() » In Loop 'for content in raw_content:' » content")
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
    # text_maker.images_with_size = True
    text_maker.ignore_links = False
    text_maker.body_width = 0
    text_maker.ignore_tables = True
    text_maker.pad_tables = True
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
                specialPrint(new_src, "format.py > changeSrc() » srcset elif statement")
            elif img['src'].startswith('http://www.wikimotiveblogs.com') and img.has_attr('srcset'):
                new_src = str(img['srcset'].split()[0])
                img_src_list.append(new_src)
                srcset_count += 1
                specialPrint(new_src, "format.py > changeSrc() » srcset elif statement")
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
    specialPrint(str(image_source_score),"format.py > changeSrc() » image_source_scores")

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
    new_links = testFirstTwoImages(new_links)
    print(str(len(new_links)) + " Image Links on This Page!")
    print(new_links)
    # The below loop should adjust the image source to be the DI image
    #new_links_count = len(new_links)
    link_index = 0
    #We ensure the lists match up by using the same search parameters as the previous for loop...
    #--> the same search parameters, return the same list, in the same order.
    for img in content.findAll('img'):
        try:
            specialPrint(new_links[link_index], "format.py > changeSrc() » List validtion SUCCESSFUL!")
        except:
            img_error = "ERROR IN SRC REPLACEMENT -- Link Index:" + str(link_index) + "new_links:" + str(img)
            # GSP[title]['error_list'].append(img_error)
            return content
        if new_links == []:
            #print('changeSrc Loop 2: EMPTY LIST')
            return content
        elif img.has_attr('src') and img['src'] is not None:
            #print(img['src'])
            di_image_url = addDashOneToImage(str(new_links[link_index]))
            img['src'] = di_image_url
            #print(img['src'])
            link_index += 1
        elif img.has_attr('data-src') and img['data-src'] is not None:
            #print(img['data-src'])
            di_image_url = addDashOneToImage(str(new_links[link_index]))
            img['data-src'] = di_image_url
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
    try:
        #remove extra <h1> tags if found
        title = soup.find('h1')
        if title:
            title.decompose()
            specialPrint("SUCCESS - <h1> Tag Removed", "format.py > remove_extra_title()")
            return soup
        else:
            return soup
    except:
        specialPrint("FAILURE - <h1> Tag Removal broke the script", "format.py > remove_extra_title()")
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
    selector_list = config.LIVE_SELECTOR_ID
    raw_soup = soup
    for selector in selector_list:
        try:
            text_content = soup.find(selector[0], {selector[1]: selector[2]})
            link_list = soup.find_all('a')
            for link in link_list:
                url = str(link['href']).lower()
                print(url)
                #if "wikimotiveblogs" in url:
                    #do something about it
                href_string = remove_internal_domain(url)
                if "wikimotiveblogs.com" in href_string:
                    href_string = ""
                link['href'] = href_string.lower()
                # if href_string == url:
                #     specialPrint("URL Match Found!", "format.py > find_a_tags(soup)")
                #     link['target'] = '_blank'
                #     print(link)
                specialPrint("SUCCESS - Slug Replaced!", "format.py > find_a_tags(soup)")
        except:
            specialPrint("FAILURE - Replacing Slug failed", "format.py > find_a_tags(soup)")
            # GSP[title]['error_list'].append("Issue Finding <a> Tags: " + title)
    return soup

def find_iframes(soup):
    print("›››--------format.find_iframes called--------")
    raw_soup = soup
    # selector_list = [['main','class','js-layout-main-block'],['div','class','blogContent']]
    try:
        #text_content = soup.find(selector[0], {selector[1]: selector[2]})

        iframe_list = soup.find_all('iframe')
        counter = 0
        for iframe in iframe_list:
            parent = iframe.parent
            iframe_string = format_iframe(iframe)
            iframe.decompose()
            parent.string = iframe_string
            #print(parent)
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

def check_url_for_domain(url):
    print("›››------- Checking URL for domain name-------")
    domain = "https://www." + config.LIVE_SITE_DOMAIN + ".com"
    unsecure_domain = "http://www." + config.LIVE_SITE_DOMAIN + ".com"
    if domain in url:
        return [True, str(domain)]
    elif unsecure_domain in url:
        return [True, str(unsecure_domain)]
    else:
        #else, it regurgitates the original url
        return [False, url]

#Checks if the domain for the url is the same as the one for the site we are migrating from
def remove_internal_domain(url):
    print("›››------- In 'remove_internal_domain(url)' -------")
    #if it is the same, if deletes it and returns just the slug
    response_array = check_url_for_domain(url)
    if response_array[0]:
        slug = url.replace(response_array[1], '')
        slug = remove_fileypes_from_slug(slug)
        # slug = audit_href_slug(slug)
        if str(slug[-1]) != "/":
            slug = str(slug) + '/'
        return slug
    else:

        #else, it regurgitates the original url
        return url


def remove_fileypes_from_slug(url):
    print("›››------- Trying to swap Filetypes with a backslash-------")
    filetypes = ['.html','.htm','.aspx']
    for item in filetypes:
        if item in str(url):
            slug = url.replace(item,'')
            return slug
    return url

def audit_href_slug(url):
    #splits
    elem = ""
    og_url = url
    if "." in url:
        specialPrint(">>> Removing the slug from the url","format.py > audit_href_slug(url)")
        elems = url.split('.')

        return elem
    else:
        specialPrint(">>> No Chanes made to url","format.py > audit_href_slug(url)")
        return og_url

# def addTargetToLink(a_tag):
#     try:
#         print('››› in "addTargetToLink(a_tag)"')
#         print(a_tag['href'])
#         a_tag['target'] = "_blank"
#         return a_tag
#     except:
#         specialPrint("FAILURE - Adding _blank to <a> tag broke script", "format.py > addTargetToLink(a_tag)")
#         return a_tag

def replace_alt_text(title):
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
    print(iframe)
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
        print("››› Generic Iframe Found")
        generic_shell = """
        <div class="text-center main-iframe"><iframe src="{0}" frameborder="0" scrolling="auto" width="100%" height="{1}"></iframe></div>
        <div class="text-left">Is the tool above not loading on the page? <a href="{0}" target="_blank">Click Here to open it in a new tab <i class="fa fa-chevron-right" aria-hidden="true"></i></a></div>
        <br/><br/>"""
        try:
            generic_shell = generic_shell.format(iframe['src'],iframe['height'])
            iframe_shell = generic_shell
        except:
            generic_shell = generic_shell.format(iframe['src'],"950px")
            iframe_shell = generic_shell
    return iframe_shell


def replace_consistent_images(soup):
        try:
            #finds the <a> tag that surrounds the thumbnail image
            img_tags = soup.findAll('img')
            for img in img_tags:
                result = confirmImageIsIcon(str(img['src']))
                parent_tags = img.parents
                for parent in parent_tags:
                    print(parent.name)
                if result:

                    specialPrint("SUCCESS - Icon Image Removed", "format.py > replace_consistent_images()")
            return soup
        except:
            specialPrint("FAILURE - Replacing the icons broke the script", "format.py > replace_consistent_images()")
            return soup

def confirmImageIsIcon(img_url):
    index = 0
    banned_list = ["/performance[0-9]{2,4}\.png$",
    "exterior[0-9]{2,4}\.png$",
    "technology[0-9]{2,4}\.png$"]
    svg_list = ['mechanical_options', 'car', 'wifi']
    for slug in banned_list:
        link_match = re.search(slug, img_url)
        if link_match:
            #do something with the link
            #content = '[di_svg name="{}" height="25" width="32" fill="1c66b3"]'.format(svg_list[index])
            return content
        else:
            #increase count by 1 and keep looking for a match
            index += 1
    #if no match is found return a negative (or the same url)
    return False

def remove_duplicate_image(soup):
    try:
        #finds the <a> tag that surrounds the thumbnail image
        img_tags = soup.findAll('img')
        if len(img_tags) > 1:
            thumbnail = img_tags[0]
            #gets the url of that image from the 'src' attribute
            thumbnail_url = str(thumbnail['src'])
            thumbnail_parent = thumbnail.parent
            #thumbnail_name = download.splitString(thumbnail_url, '/')[-1]
            #gets the specific file name from that url
            next_image_url =  str(img_tags[1]['src'])
            if thumbnail_url[:-12] == next_image_url[:-12]:
                thumbnail_parent.decompose()
                specialPrint("SUCCESS - Thumbnail Removed", "format.py > remove_duplicate_image()")
                return soup
            else:
                specialPrint("SUCCESS - Thumbnail Not Removed but script didn't break!", "format.py > remove_duplicate_image()")
                return soup
        else:
            specialPrint("SUCCESS - Thumbnail is the only image on the post! Nothing removed", "format.py > remove_duplicate_image()")
            return soup
    except:
        specialPrint("FAILURE - Trying to Decompose the thumbnail broke the script", "format.py > remove_duplicate_image()")
        return soup



#checks the first two images in the array to make sure we don't have duplicates
def testFirstTwoImages(img_array):
    try:
        first_image = str(img_array[0])
        second_image = str(img_array[1])
        first_name = first_image.split('/')[-1]
        second_name = second_image.split('/')[-1]
        if first_name == second_name:
            specialPrint("_♦_| SUCCESS - Duplicate Found", "format.py > testFirstTwoImages(img_array)")
            new_array = img_array[1:]
            return new_array
        else:
            return img_array
    except:
        specialPrint("FAILURE - image test broke the script", "format.py > testFirstTwoImages(img_array)")
        return img_array


#if the image ends with specific pixel sizes, this function appends it with a "-1" to match wordpress's automatic naming adjustments
def testImageUrl(img_url):
    url = str(img_url)
    is_found = re.search("[0-9]{3,4}x[0-9]{3,4}\.jpg$", url)
    if is_found:
        return True
    else:
        return False

def addDashOneToImage(img_url):
##    pixel_text = img_url[-11:]
##    segment = re.match("[0-9]{3,4}x[0-9]{3,4}\.jpg$", pixel_text)
    full_link = testImageUrl(img_url)
    if full_link:
        print("_♦_| Match Found - Adding '-1' to the image name")
        new_link = img_url.replace(".jpg","-1.jpg")
        #print(new_link)
        return new_link
    else:
        return img_url



def remove_picture_tag(soup):
    try:
        index = 0
        div_tags = soup.findAll('div',{'class','widget-image'})
        for tag in div_tags:
            try:
                pic = tag.picture
                img = tag.picture.img
                new_img = format_image(get_source_url(img), img['alt'])
                pic.decompose()
                tag.string = new_img
                print(new_img)
                specialPrint("SUCCESS - Tag replaced", "format.py > remove_picture_tag()")
                index += 1
            except:
                continue
        return soup
    except:
        specialPrint("FAILURE - Tag not replaced :(", "format.py > remove_picture_tag()")
        return soup

def format_image(img_url, img_alt):
    if img_alt == "":
        img_alt = str(getImageNameFromUrl(img_url))
    img_url = str(img_url)
    img_alt = str(img_alt)
    img_shell = '''<img src="{0}" alt="{1}" />'''.format(img_url, img_alt)
    print(img_shell)

    return str(img_shell)

def getImageNameFromUrl(img_url):
    decomp_list = ['-','_']
    file_names = img_url.split('.')
    file_ext = file_names[-2]
    file_name = file_ext.split('/')[-1]
    file_name = file_name.replace('com/','')
    for item in decomp_list:
        file_name = file_name.replace(item,' ')
    print(file_name)
    return file_name
def get_source_url(img_tag):
    try:
        img_url = str(img_tag['data-src'])
        return img_url
    except:
        try:
            img_url = str(img_tag['src'])
            return img_url
        except:
            specialPrint("FAILURE - <img> url not found :(", "format.py > get_source_url(img_tag)")
            return False



def table_markdown(text):
    markdowner = Markdown(extras=["tables"])

    htmlout = markdowner.convert(text)
    # htmlout = htmlout.replace('</strong></p> <p>\n| </p>','</td><td>')
    # htmlout = htmlout.replace('</strong></p> <p>','</td></tr><tr>')
    # htmlout = htmlout.replace('<p><strong>','<td>')
    # htmlout = htmlout.replace('<br />\n|','</td><td>')
    # htmlout = htmlout.replace('<br /> |','</td><td>')
    # htmlout = htmlout.replace('<p>','</td>')
    # htmlout = '<tr>' + htmlout + '</tr>'
    # htmlout = htmlout.replace('| ','<td>')
    return htmlout

def table_convert(raw_content):
    text_maker = html2text.HTML2Text()
    # text_maker.ignore_links = False
    # text_maker.body_width = 0
    text_maker.ignore_tables = False
    text_maker.pad_tables = False
    text = text_maker.handle(raw_content.prettify())
    text = table_markdown(text)

    return text

def soupify_TableElements(soup):
    table_elements = soup.findAll('table')
    return table_elements

def find_table_tags(soup):
    try:
        full_list = []
        table_string = "<table>\n<tbody>\n"
        if soup.find('table'):
            table_elements = soupify_TableElements(soup)
            for table in table_elements:
                print("<------------------- NEW TABLE ------------------>")
                table_parent = table.parent
                #print(table_parent)
                tr_elements = table.findAll('tr')
                #print(tr_elements)
                for row in tr_elements:
                    row_html = table_convert(row)
                    table_string = table_string + row_html
                table_string = table_string + '</tbody>\n</table>\n'
                table_parent.string = table_string
                table.decompose()
                #full_list.append(new_div.prettify())
            specialPrint('SUCCESS - Table found and formatted!', 'format.py > find_table_tags(soup)')
            return soup
        else:
            specialPrint('SUCCESS - Table function did not break anything!', 'format.py > find_table_tags(soup)')
            return soup
    except:
        specialPrint('FAILURE - trying to find the tables broke the script.', 'format.py > find_table_tags(soup)')
