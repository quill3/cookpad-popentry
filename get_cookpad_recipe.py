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

        # pattern = re.compile(r'<meta name="description" content="(.*?)" />')

        pattern = re.compile('''<div id="description" class="font14 summary">(.*?)<div class="right">''',re.S)
        parse_results2 = pattern.findall(get_result.content)
        if not parse_results2:
            parse_results2 = ['']
        else:
            parse_results2[0] = parse_results2[0].strip()

        pattern = re.compile(r'<span class="tsukurepo_count">(.*?)</span>')
        parse_results3 = pattern.findall(get_result.content)
        if not parse_results3:
            parse_results3 = ['0']

        pattern = re.compile(r'<a href="/category/(.*?)">(.*?)</a>')
        parse_results4 = pattern.findall(get_result.content)
        for temp in range(3-len(parse_results4)):
            parse_results4.append(('',''))

    else:
        parse_results1 = ['']
        parse_results2 = ['']
        parse_results3 = ['0']
        parse_results4 = [('',''),('',''),('','')]
        parse_results5 = [('','')]

    return {'entry_url':url,
            'photo_url':parse_results1[0],
            'description':unicode(parse_results2[0],'utf-8'),
            'tsukurepo_count':int(parse_results3[0]),
            'category1_id':parse_results4[0][0].replace('?class=tag', ''),
            'category1_name':unicode(parse_results4[0][1],'utf-8'),
            'category2_id':parse_results4[1][0].replace('?class=tag', ''),
            'category2_name':unicode(parse_results4[1][1],'utf-8'),
            'category3_id':parse_results4[2][0].replace('?class=tag', ''),
            'category3_name':unicode(parse_results4[2][1],'utf-8')}


def put_entry(row):
    if not row:return

    query = datastores.Entries.gql('WHERE entry_url = :url',url=row['entry_url'])
    entry = query.get()

    if not entry.photo_url == row['photo_url']:
        entry.photo_url = row['photo_url']
        entry.photo_image = get_resizedimage(row['photo_url'],100,100)
    entry.description = row['description']
    entry.tsukurepo_count = row['tsukurepo_count']
    if row['category1_id']:
        put_category(row['category1_id'],row['category1_name'],'1')
        entry.category1_id = row['category1_id']
        entry.category1_name = row['category1_name']
    if row['category2_id']:
        put_category(row['category2_id'],row['category2_name'],'2')
        entry.category2_id = row['category2_id']
        entry.category2_name = row['category2_name']
    if row['category3_id']:
        put_category(row['category3_id'],row['category3_name'],'3')
        entry.category3_id = row['category3_id']
        entry.category3_name = row['category3_name']
    entry.cookpad_checked_time = datetime.datetime.today()
    entry.put()


def get_resizedimage(url,width,height):
    if not url:return

    image_url = 'http://' + url
    get_image = urlfetch.fetch(image_url,deadline=10)

    if get_image.status_code == 200:
        return images.resize(get_image.content,width,height)


def put_category(id,name,kubun):
    query = datastores.Categories.gql('WHERE category_id = :id',id=id)
    category = query.get()

    if not category:
        category = datastores.Categories()
        category.category_id = id
        category.category_name = name
        category.category_kubun = kubun
        category.hit_count = 0
        category.put()


if __name__ == "__main__":
    put_entry(get_recipe(get_entry()))