#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# About the app
#

import datetime
import time
import os
import re
import email.utils
import calendar
import logging
from xml.dom import minidom
import urllib
from django.utils import simplejson
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext.webapp import util
import AppConfig
from UserString import MutableString

#main controller
class AboutAppHandler(webapp.RequestHandler):
    def get(self):
		
		template_values = { 
						   }
		path = os.path.join(os.path.dirname(__file__), 'templates')
		path = os.path.join(path, 'about.html')
		self.response.out.write(template.render(path, template_values))