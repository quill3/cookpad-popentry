#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
from google.appengine.api import images

import re
import datetime

import datastores


def get_entry():
    query = datastores.Entries.gql('ORDER BY cookpad_checked_time ASC')
    entry = query.get()

    if entry:
        return entry.entry_url


def get_recipe(url):
    if not url:return

    recipe_url = 'http://' + url
    get_result = urlfetch.fetch(recipe_url,deadline=10)

    if get_result.status_code == 200:
        pattern = re.compile(r'<img alt="メイン画像" class="photo" src="http://(.*?)"')
        parse_results1 = pattern.findall(get_result.content)
        if not parse_results1:
            parse_results1 = ['']

        pattern = re.compile(r'<meta name="description" content="(.*?)" />')
        parse_results2 = pattern.findall(get_result.content)
        if not parse_results2:
            parse_results2 = ['']

        pattern = re.compile(r'<span class="tsukurepo_count">(.*?)</span>')
        parse_results3 = pattern.findall(get_result.content)
        if not parse_results3:
            parse_results3 = ['0']

        pattern = re.compile(r'<a href="/category/(.*?)">(.*?)</a>')
        parse_results4 = pattern.findall(get_result.content)
        if not parse_results4:
            parse_results4 = [('','')]

        pattern = re.compile(r'<a href="/category/(.*?)\?class=tag">(.*?)</a>')
        parse_results5 = pattern.findall(get_result.content)
        if not parse_results5:
            parse_results5 = [('','')]

    else:
        parse_results1 = ['']
        parse_results2 = ['']
        parse_results3 = ['0']
        parse_results4 = [('','')]
        parse_results5 = [('','')]

    return {'entry_url':url,
            'photo_url':parse_results1[0],
            'description':unicode(parse_results2[0],'utf-8'),
            'tsukurepo_count':int(parse_results3[0]),
            'largecategory_id':parse_results4[0][0],
            'largecategory_name':unicode(parse_results4[0][1],'utf-8'),
            'smallcategory_id':parse_results5[0][0],
            'smallcategory_name':unicode(parse_results5[0][1],'utf-8')}


def put_entry(row):
    if not row:return

    query = datastores.Entries.gql('WHERE entry_url = :url',url=row['entry_url'])
    entry = query.get()

    if not entry.photo_url == row['photo_url']:
        entry.photo_url = row['photo_url']
        entry.photo_image = get_resizedimage(row['photo_url'],100,100)
    entry.description = row['description']
    entry.tsukurepo_count = row['tsukurepo_count']
    if row['largecategory_id']:
        entry.largecategory = get_category(row['largecategory_id'],row['largecategory_name'],datastores.LargeCategories)
    if row['smallcategory_id']:
        entry.smallcategory = get_category(row['smallcategory_id'],row['smallcategory_name'],datastores.SmallCategories)
    entry.cookpad_checked_time = datetime.datetime.today()
    entry.put()


def get_resizedimage(url,width,height):
    if not url:return

    image_url = 'http://' + url
    get_image = urlfetch.fetch(image_url,deadline=10)

    if get_image.status_code == 200:
        return images.resize(get_image.content,width,height)


def get_category(id,name,Categories):
    query = Categories.gql('WHERE id = :id',id=id)
    category = query.get()

    if not category:
        category = Categories()
        category.id = id
        category.name = name
        category.hit_count = 0
        category.put()
    return category


if __name__ == "__main__":
    put_entry(get_recipe(get_entry()))

##unit test code : get_entry method
#    print get_entry()

##unit test code : get_recipe method
##recipe id:1121500/1317264/1373581/1661
#    print 'test of get_recipe'
#    print get_recipe('cookpad.com/recipe/1661')

##unit test code : put_entry method
#    row = {'largecategory_id': '123',
#           'largecategory_name': u'ふがふが',
#           'smallcategory_id': '456',
#           'smallcategory_name': u'ららら',
#           'photo_url': 'img6.cookpad.com/recipe/p/1889/858/5BAFC8617E9932B314D6A484BCA8AEDD.jpg?1273502049',
#           'tsukurepo_count': 516,
#           'description': u'ほげほげ',
#           'entry_url': 'cookpad.com/recipe/252807'}
#    put_entry(row)

##unit test code : get_resizedimage method
#    print get_resizedimage('img7.cookpad.com/recipe/p/373/786/D936E58B7B6230D5B65A2EE6CA1DE452.jpg?1292597022',100,100)

##unit test code : get_category method
#    get_category('112',u'あああ',datastores.LargeCategories)