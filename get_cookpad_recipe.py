#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch

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

        pattern = re.compile(r'<a href="/category/(.*?)class=tag">(.*?)</a>')
        parse_results4 = pattern.findall(get_result.content)
        if not parse_results4:
            parse_results4 = [('','')]

        return {'entry_url':url,
                'photo_url':parse_results1[0],
                'description':unicode(parse_results2[0],'utf-8'),
                'tsukurepo_count':int(parse_results3[0]),
                'category':unicode(parse_results4[0][1],'utf-8')}


def put_entry(row):
    if not row:return

    query = datastores.Entries.gql('WHERE entry_url = :url',url=row['entry_url'])
    entry = query.get()

    entry.photo_url = row['photo_url']
    entry.description = row['description']
    entry.tsukurepo_count = row['tsukurepo_count']
    entry.category = row['category']
    entry.cookpad_checked_time = datetime.datetime.today()
    entry.put()


if __name__ == "__main__":
    put_entry(get_recipe(get_entry()))

##unit test code : get_entry method
#    print get_entry()

##unit test code : get_recipe method
##recipe id:1121500/1317264/1373581
#    print 'test of get_recipe'
#    print get_recipe('cookpad.com/recipe/1121500')

##unit test code : put_entry method
#    row = {'category': u'ふがふが',
#           'photo_url': 'img6.cookpad.com/recipe/p/1889/858/5BAFC8617E9932B314D6A484BCA8AEDD.jpg?1273502049',
#           'tsukurepo_count': 516,
#           'description': u'ほげほげ',
#           'entry_url': 'cookpad.com/recipe/1121500'}
#    put_entry(row)
