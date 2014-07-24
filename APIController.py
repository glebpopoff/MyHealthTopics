#!/usr/bin/env python

#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# API Controller: lists all API and allows user to quickly test/use supported APIs
#

import datetime
import time
import os
import email.utils
import calendar
import logging
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
import AppConfig

# api main controller
class APIHandler(webapp.RequestHandler):
    def get(self):
		#set django html template vars			
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'templates')
		path = os.path.join(path, 'api.html')
		self.response.out.write(template.render(path, template_values))