#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, time, json, base64, pprint, Live_Urls, scrape
#TODO: Change Yoast Meta https://developer.yoast.com/blog/yoast-seo-rest-api-endpoint/
#       1. Scrape meta
#       2. getPostID of page
#       3. send edits to rest endpoint

#TODO: Make this work for blogs. It should basically function the same but you'll need to scrape
#      date-of-publish, categrory, & tags

#TODO: Save Place
devsite = 'http://contentdevsandbox.dev.dealerinspire.com/'
live_urls = Live_Urls.urlsToMigrate('1L2gDfkfpoubgKtlcMVn5d0R9PpXR54kQztDWy2O7Ov4')
#live_blogs = Live_Urls.urlsToMigrate('1nayRdiuQUQcvHK5LYA_CoEYpNPuHKdS2ybhdmY_cxS0')
#'19fSBX26VrTMT5u9n34t0PWrT1Bnx-nYPckTpd3M1LtY')
#blog1
for url in live_urls:
    scrape.livePage(url, 'content1', devsite)
    time.sleep(2)
