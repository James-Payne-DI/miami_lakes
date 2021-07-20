#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json

def getContent(dictionary):
    return dictionary.get('content').get('rendered')

def getPostId(dictionary):
    return dictionary.get('id')

def getTitle(dictionary):
    return dictionary.get('title').get('rendered')

def getPostType(dictionary):
    return dictionary.get('type')

def getFeaturedMedia(dictionary):
    return dictionary.get('featured_media')

def getSourceUrl(dictionary):
    return dictionary.get('source_url')

def getLink(dictionary):
    return dictionary.get('link')

def getDate(dictionary):
    return dictionary.get('date')

def getSlug(dictionary):
    return dictionary.get('slug')

def getPostStatus(dictionary):
    return dictionary.get('status')

def getDateGMT(dictionary):
    return dictionary.get('date_gmt')

def getAttachmentsEndpoint(dictionary):
    return dictionary.get('_links').get('wp:attachment')[0].get('href')

def getTemplate(dictionary):
    return dictionary.get('template')

def getPostMeta(dictionary):
    post_meta = dictionary.get('post_meta')
    return post_meta

def formatPageJson(dictionary):
    data = \
    {
        "date": getDate(dictionary),
        "date_gmt": getDateGMT(dictionary),
        "slug": getSlug(dictionary),
        "status": getPostStatus(dictionary),
        "type": getPostType(dictionary),
        "template": getTemplate(dictionary),
        "title": getTitle(dictionary),
        "content": getContent(dictionary)

    }
    data = json.dumps(data)
    return data

def formatPostMeta(dictionary):
    nested_meta = getPostMeta(dictionary)
    post_meta = \
    {
        "post_meta": json.dumps({k:v for (k,v) in nested_meta.items()})
    }

    return post_meta

def formatFeaturedImage(image_id):
    post_meta = \
    {
        "featured_media": image_id
    }
    return post_meta
