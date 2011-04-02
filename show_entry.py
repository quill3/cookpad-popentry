#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import os
import datetime
import re

import datastores


class MainPage(webapp.RequestHandler):
    def get(self):
        inputparm = get_inputparm(self)
        showparm = get_showparm()
        checkedparm = check_parm(inputparm,showparm)
        gqlsentence = make_gqlsentence(checkedparm)

        # self.response.out.write(gqlsentence)

        query = datastores.Entries.gql(gqlsentence)
        fetched_entries = query.fetch(25,int(checkedparm['offset']))

        template_values = { 'entries' : fetched_entries,
                                        'showparm' : showparm,
                                        'inputparm' : checkedparm}

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class ThumbNail (webapp.RequestHandler):
    def get(self):
        entry = datastores.Entries.get(self.request.get("key"))
        if entry.photo_image:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(entry.photo_image)
        else:
            self.error(404)


def get_inputparm(self):
    inputparm = {}
    for p in ['category','year','season','sort','offset']:
        inputparm[p] = str(self.request.get(p))
    return inputparm

def get_showparm():
    category1 = get_categorylist('1')
    category2 = get_categorylist('2')

    startyear = 2008
    endyear = datetime.datetime.today().year + 1
    year = [[str(y),str(y)] for y in range(startyear,endyear)]

    season = [['spring',u'春'],['summer',u'夏'],['autumn',u'秋'],['winter',u'冬']]

    sort = [['bukuma_count',u'ブクマ数順'],['tsukurepo_count',u'つくれぽ数順'],['hateb_added_date',u'新着順']]

    return {'category1' : category1,
                'category2' : category2,
                'year' : year,
                'season' : season,
                'sort' : sort}

def get_categorylist(kubun):
    query = datastores.Categories.gql("WHERE category_kubun = '" + kubun + "' ORDER BY hit_count DESC")
    fetched_categories = query.fetch(30)
    return [[c.category_id,c.category_name] for c in fetched_categories]

def check_parm(inputparm,showparm):
    checkedparm = {}

#デフォルト値
    for p in ['category1_id','category2_id','category_name','year','season']:
        checkedparm[p] = ""
    checkedparm['sort'] = "bukuma_count"
    checkedparm['offset'] = "0"

    for k, v in inputparm.iteritems():
        if k == 'category':
#categoryは半角数字のみ
            if is_num(v):
#categoryの存在チェック、区分と名称を取得、ヒット数をカウントアップ
                query = datastores.Categories.gql("WHERE category_id = '" + v + "'")
                category = query.get()
                if category:
                    key = 'category' + category.category_kubun + '_id'
                    checkedparm[key] = v
                    checkedparm['category_name'] = category.category_name
                    category.hit_count += 1
                    category.put()
        elif k == 'offset':
#offsetは半角数字のみ
            if is_num(v):
                checkedparm[k] = v
        else:
#year,season,sortはshowparmと一致していること
            for p in showparm[k]:
                if v == p[0]:
                    checkedparm[k] = v
                    break
    return checkedparm

def is_num(v):
    if not v:
        return False
    pattern = re.compile(r'[^0-9]')
    if pattern.search(v):
        return False
    return True

def make_gqlsentence(parm):
    gqlsentence = ""
    i = 0
    for p in ['category1_id','category2_id','year','season']:
        if parm[p]:
            if i == 0:
                gqlsentence = gqlsentence + "WHERE "
                i = 1
            else:
                gqlsentence = gqlsentence + "AND "
            gqlsentence = gqlsentence + p + " = '" + parm[p] + "' "

    gqlsentence = gqlsentence + "ORDER BY " + parm['sort'] + " DESC"

    return gqlsentence


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/tn', ThumbNail)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()