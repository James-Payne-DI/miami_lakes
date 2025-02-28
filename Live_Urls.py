import csv, io, requests, urllib3
from urllib.parse import urlparse, urlunparse
import config

def urlsToMigrate(google_sheet_id):
    pages = []
    slugs = []
    url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(google_sheet_id)
    print(url)
    urllib3.disable_warnings()
    r = requests.get(url,verify=False)
    sio = io.StringIO(r.text, newline=None)
    reader = csv.reader(sio, dialect=csv.excel)

    for row in reader:
        slugs.append(swapInternalSlug(row[0]))
        pages.append(row[0])
        print(row[0])

    config.SLUG_LIST = slugs
    #print(config.SLUG_LIST)
    return pages

def swapInternalSlug(url):
    try:
        url_pieces_uno = url.split('.')
        url_domain = url_pieces_uno[1]
        if domain_check(url_domain):
            url_pieces = url.split('/')
            slug = url_pieces[-1]
            slug = slug.replace('com/2','2')
            print("--» Post Slug: " + slug)
            return slug

    except:
        print("Issue Finding slug for: " + url)
        return url

def domain_check(url_domain):
    if config.LIVE_SITE_DOMAIN == url_domain:
        return True
    else:
        return False




def transform_url(original_url):
    """
    Transforms a blog post URL into the desired format.
    
    Args:
        original_url (str): The original blog post URL.
    
    Returns:
        str: The transformed URL.
    """
    try:
        # Parse the original URL
        parsed_url = urlparse(original_url)
        
        # Extract the article slug (the last part of the path)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 5:
            raise ValueError("URL path does not have the expected format.")
        article_slug = path_parts[-1]
        article_slug = article_slug.replace(".htm","")
        
        # Construct the new netloc (domain) and path
        new_netloc = "aaronchevrolet.dev.dealerinspire.com"
        new_path = f"/{article_slug}/"
        
        # Rebuild the URL
        transformed_url = urlunparse((
            parsed_url.scheme,  # Scheme (e.g., "https")
            new_netloc,         # New domain
            new_path,           # New path
            "",                 # Params (empty)
            "",                 # Query (empty)
            ""                  # Fragment (empty)
        ))
        
        return transformed_url
    except Exception as e:
        return f"Error transforming URL: {e}"


# Example Usage
#original_url = "https://www.aaronchevy.com/blog/2024/december/12/7-weekend-getaways-near-lake-elsinore-california.htm"
# url_list = urlsToMigrate('1VXx4krWXik0q_Viu1hHt8e97P76z1Y1zg4zx2SdTA8A')
# for original_url in url_list:
#     transformed_url = transform_url(original_url)
#     print(transformed_url)


