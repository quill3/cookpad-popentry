#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch

import re
import datetime

import datastores


def get_counter():
    query = datastores.Counter.gql('')
    counter = query.get()

    if not counter:
        counter = datastores.Counter()
        counter.counter = 0
        counter.put()

    return str(counter.counter)


def get_entrylist(url,sort='count',offset='0'):
    entrylist_url = 'http://b.hatena.ne.jp/entrylist?sort=' + sort + '&url=' + url + '&of=' + offset
    get_result = urlfetch.fetch(entrylist_url,deadline=10)

    if get_result.status_code == 200:
        pattern = re.compile(r'''<li class="users"> <strong><a href="/entry/(.*?)" title="はてなブックマーク - (.*?) \((.*?)ブックマーク\)">(.*?) users</a></strong></li>
        <li class="timestamp">(.*?)</li>''',re.S)
        parse_results = pattern.findall(get_result.content)

        return [{'entry_url':row[0],
                 'entry_title':unicode(row[1],'utf-8'),
                 'bukuma_count':int(row[3]),
                 'hateb_added_date':date_string_to_obj(row[4])} for row in parse_results]


def put_entry(row):
    query = datastores.Entries.gql('WHERE entry_url = :url',url=row['entry_url'])
    entry = query.get()

    if entry:
        if not entry.bukuma_count == row['bukuma_count']:
            entry.bukuma_count = row['bukuma_count']
            entry.put()
    else:
        entry = datastores.Entries()
        entry.entry_url = row['entry_url']
        entry.entry_title = row['entry_title']
        entry.bukuma_count = row['bukuma_count']
        entry.hateb_added_date = row['hateb_added_date']
        entry.year = str(row['hateb_added_date'].year)
        entry.season = get_season(row['hateb_added_date'].month)
        entry.photo_url = ''
        entry.description = ''
        entry.category1_id = ''
        entry.category1_name = ''
        entry.category2_id = ''
        entry.category2_name = ''
        entry.category3_id = ''
        entry.category3_name = ''
        entry.tsukurepo_count = 0
        entry.cookpad_checked_time = datetime.datetime(2011,1,1)
        entry.put()


def put_counter(upcount=0):
    query = datastores.Counter.gql('')
    counter = query.get()

    if upcount > 0:
        counter.counter = counter.counter + upcount
    else:
        counter.counter = 0
    counter.put()


def date_string_to_obj(date_string):
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])

    return datetime.datetime(year,month,day)


def get_season(month):
    if month in (3,4,5):
        return 'spring'
    elif month in (6,7,8):
        return 'summer'
    elif month in (9,10,11):
        return 'autumn'
    else:
        return 'winter'


if __name__ == "__main__":
    upcount = 0
    for row in get_entrylist('http://cookpad.com/recipe/','count',get_counter()):
        endpoint = row['entry_title'].find(u' [クックパッド]')
        if endpoint > -1:
            row['entry_title'] = row['entry_title'][0:endpoint]

        if row['bukuma_count'] >= 5:
            put_entry(row)
            upcount += 1
        else:
            upcount = 0
            break
    put_counter(upcount)