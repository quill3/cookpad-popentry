#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import os

import datastores

class MainPage(webapp.RequestHandler):
    def get(self):
        query = datastores.Entries.gql('ORDER BY bukuma_count DESC')
        fetched_entries = query.fetch(25)

        template_values = { 'entries' : fetched_entries }

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

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/tn', ThumbNail)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
