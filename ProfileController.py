#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Profile Controller
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

class ProfileAppHandler(webapp.RequestHandler):
    def get(self):
		appIDValue = ""
		#check cookie container
		if (AppConfig.appCookieName in self.request.cookies):
			#get application ID from cookies
			appIDValue = self.request.cookies[AppConfig.appCookieName]
		
		#set django html template vars			
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'templates')
		path = os.path.join(path, 'profile.html')
		self.response.out.write(template.render(path, template_values))