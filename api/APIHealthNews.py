#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Health News RESTful API Service
# The health news are retrieved from the RSS service: 
# English: http://www.nlm.nih.gov/medlineplus/feeds/news_en.xml
# Spanish: http://www.nlm.nih.gov/medlineplus/feeds/news_es.xml
#
# URL: /api/healthnews/lan/(en|es)/format/json
# Example (English): /api/healthnews/lan/en/format/json
# The [language] is either en or es. The service returns health news in english or spanish
#

import re
import logging
from UserString import MutableString
from google.appengine.api import urlfetch
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
import Formatter
import AppConfig
import UtilLib
from xml.sax.saxutils import escape
from api import APIUtils

# class definition
class GetHealthNewsHandler(webapp.RequestHandler):
	#controller main entry		
	def get(self,lan='en',format='json'):
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		returnData = MutableString()
		returnData = APIUtils.getHealthNews(lan,format)
					
		#output to the browser
		self.response.out.write(Formatter.dataWrapper(format, returnData))