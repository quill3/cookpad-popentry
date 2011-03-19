#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Counter(db.Model):
    counter = db.IntegerProperty()

class LargeCategories(db.Model):
    id = db.StringProperty()
    name = db.StringProperty()
    hit_count = db.IntegerProperty()

class SmallCategories(db.Model):
    id = db.StringProperty()
    name = db.StringProperty()
    hit_count = db.IntegerProperty()

class Entries(db.Model):
    entry_url = db.StringProperty()
    entry_title = db.StringProperty(multiline=True)
    bukuma_count = db.IntegerProperty()
    hateb_added_date = db.DateTimeProperty()
    photo_url = db.StringProperty()
    photo_image = db.BlobProperty()
    description = db.StringProperty()
    largecategory = db.ReferenceProperty(LargeCategories)
    smallcategory = db.ReferenceProperty(SmallCategories)
    tsukurepo_count = db.IntegerProperty()
    cookpad_checked_time = db.DateTimeProperty()