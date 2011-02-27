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
    photo_url = db.StringProperty()
    description = db.StringProperty()
    category = db.StringProperty()
    tsukurepo_count = db.IntegerProperty()
    cookpad_checked_time = db.DateTimeProperty()
