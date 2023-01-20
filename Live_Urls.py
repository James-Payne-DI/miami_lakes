import csv, io, requests, urllib3
import config

def urlsToMigrate(google_sheet_id):
    pages = []
    slugs = []
    url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(google_sheet_id)
    urllib3.disable_warnings()
    r = requests.get(url,verify=False)
    sio = io.StringIO(r.text, newline=None)
    reader = csv.reader(sio, dialect=csv.excel)

    for row in reader:
        slugs.append(swapInternalSlug(row[0]))
        pages.append(row[0])

    config.SLUG_LIST = slugs
    print(config.SLUG_LIST)
    return pages

def swapInternalSlug(url):
    try:
        url_pieces_uno = url.split('.')
        url_domain = url_pieces_uno[1]
        if domain_check(url_domain):
            url_pieces = url.split('/')
            slug = url_pieces[-1]
            slug = slug.replace('com/2','2')
            print("--» Post Slug: " + new_slug)
            return new_slug

    except:
        print("Issue Finding slug for: " + url)
        return url

def domain_check(url_domain):
    if config.LIVE_SITE_DOMAIN == url_domain:
        return True
    else:
        return False
