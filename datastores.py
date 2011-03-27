#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Counter(db.Model):
    counter = db.IntegerProperty()

class Entries(db.Model):
    entry_url = db.StringProperty()
    entry_title = db.StringProperty(multiline=True)
    bukuma_count = db.IntegerProperty()
    hateb_added_date = db.DateTimeProperty()
    year = db.StringProperty()
    season = db.StringProperty()
    photo_url = db.StringProperty()
    photo_image = db.BlobProperty()
    description = db.StringProperty()
    category1_id = db.StringProperty()
    category1_name = db.StringProperty()
    category2_id = db.StringProperty()
    category2_name = db.StringProperty()
    category3_id = db.StringProperty()
    category3_name = db.StringProperty()
    tsukurepo_count = db.IntegerProperty()
    cookpad_checked_time = db.DateTimeProperty()

class Categories(db.Model):
    category_id = db.StringProperty()
    category_name = db.StringProperty()
    category_kubun = db.StringProperty()
    hit_count = db.IntegerProperty()