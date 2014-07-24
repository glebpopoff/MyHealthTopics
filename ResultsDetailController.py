#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Search Result Detail Screen Controller
#

import datetime
import time
import os
import email.utils
import calendar
import logging
from UserString import MutableString
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
import AppConfig

class ResultsDetailAppHandler(webapp.RequestHandler):
    def get(self):
		jsonData = MutableString()
		jsonData = '"status": "success"'
		self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
		self.response.out.write("{\"results\":[%s]}" % jsonData)