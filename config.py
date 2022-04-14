#gitHub
GITHUB_TOKEN = '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'
ATOM_GIT_TOKEN = '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'

#REST API - Sandbox: QTHa Eajf 0eAO Mhvj fuTO iXwA
#Sandbox2: "Asbury Test" = 2s7P 4I4w MjNj 0Hrh UqeF nGTo
DI_USER = 'di_dashboard'
DI_PASSWORD = '2s7P 4I4w MjNj 0Hrh UqeF nGTo'

#Devsite Link  ---- replace me
DEVSITE_URL = 'https://contentdevsandbox2.dev.dealerinspire.com/'
#Google Sheet List ---- replace me
GOOGLE_SHEET_ID = '1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko'

#Selenium
DEVSITE_USERNAME = 'dealerinspire'
DEVSITE_PASSWORD = '5IqX0HvJtpXZnqVPkOn7S22MxwGK8yKF'


#targets:
#main.py selector [HTML tag, Attribute, SelectorID]---- replace me
LIVE_SELECTOR_ID = ['div','class',"abg-static-seo-text"]

#class names of items we don't want to include (defaults  are forms, phone numbers/contact info, hours)
DECOMP_IDS = [
    ['div','data-widget-name',"contact-form"],
    ['div','data-widget-name',"contact-info"],
    ['div','data-widget-name',"hours-default"],
    ['h1','role','heading']
    ]


#dealer info dictionary -- MUST BE FILLED OUT
dealership_name = "Coggin Honda St. Augustine"
dealership_city = "St. Augustine"
dealership_state = 'FL'
dealership_salesPhone = '904-747-8228'
dealership_servicePhone = '904-747-8228'
dealership_partsPhone = '904-747-8228'

#past Targets:
#QTHa Eajf 0eAO Mhvj fuTO iXwA - Name: "Coggin Honda St. Augustine" (on Sandbox)
#Google Sheet: 1esZdhi_eZQ0T2oD5lYH57octn4H0yBaZO2K17S3NRTw
#HTML/Tag/Selector:  div/class/"abg-static-seo-text"


#JqcZ VF0h fmQq vJbo XSbF s1ND - Wayne Ford
#1mXbUcAEbjoTEL7Lz6XK_SvCK0VGnsxPJStZ1OHanMGQ


#Google Sheet: 1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko
#Jimbos Robot --- West Herr Auto Group--- gudX fSL9 hI97 NUOl sD3b aumk
#Tag/Selector:  class/"entry-content"

#Google Sheet: 1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko
#Jimbos Robot --- Performance Ford Lincoln Bountiful--- Wx4f SNN0 hMCP 8DpP L2f6 onVI
#Tag/Selector:  id/"content-main"

#Google Sheet: 1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko
#Jimbos Robot --- Safford Ford of Salisbury --- Wx4f SNN0 hMCP 8DpP L2f6 onVI
#Tag/Selector:  id/"content-main"


#Google Sheet: 1ZgEao-n_rzIdi7jw0ntU71O5kjvB5VnSi8AUpCf04JE
#Garver The Pirate --- Friendly Ford --- V0zH KOTt G7Fm OV3F dhKX qiO3
#Tag/Selector:  id/"page-body"


#Jimbos Robot --- Dwayne Lane's Skagit Ford --- xNdt nmfh INS4 Xfus Jb9j LfoP


#Jimbos Robot --- Capistrano Ford --- tIAc 38ha sec5 Fmsq j3Vd hqf9
#google sheet: 1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko
# Selectors: "# Selectors: "page-body""

#Queen Kelly --- Auffenberg Ford South  Belleville --- EeAj FXx6 Tsi6 ClJk K0j6 09qL
#Queen Kelly --- Auffenberg Ford North --- A8oD tb30 zmqY DjCw gHeY 3bZh
# Selectors: "page-body"


#Jimbos Robot --- Tim Dahle Ford --- 9Rcm t6IB peyh ZKPX WgS0 Av1E
#GoogleSheet: 1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko
# Selectors: "page-body"



#James Bond --- Terry Labonte Chevrolet --- XERi opED yACB LvFr 9XjZ 6O6n

#DI_PASSWORD = 'j1SS 9Xsp SXcd NVMH ybS3 1o9H'
#easyPeasy --- Tom Masano Ford --- j1SS 9Xsp SXcd NVMH ybS3 1o9H
# Google Sheet:  '1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko'
# Selectors:

# Google Sheet:  '1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko'
#easyPeasy --- Kemna Auto Center --- zrn1 fZ3i nd93 YvOZ gE2v X0Zz
# Selectors: 'content1'

#United Nissan:
# Google Sheet: `1Nvy0WUsBJ0CG_INiGFCfzuyvEl8nCzMdvdY7k26LFko`
# Selectors: 'fullcontentrow'
# Scrape.GetContent: raw_content = soup.findAll('div', {'class': selectors})
#Scrape.SaniSoup: for div in soup.findAll("div", {'class': 'container-fluid'}):
#^ using 'container-fluid' to target the hero image row from the DIPC page

#Steve Landers Toyota:
# Google Sheet: `1L2gDfkfpoubgKtlcMVn5d0R9PpXR54kQztDWy2O7Ov4`
# Selectors: 'content1'
# Scrape.GetContent: raw_content = soup.findAll('div', {'data-widget-id': selectors})
# Scrape.SaniSoup: (You hear the voice of the Borg Collective respond, "Irrelevant, all will be assimilated")
