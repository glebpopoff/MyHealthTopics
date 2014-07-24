#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Share This Controller
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
class ShareThisAppHandler(webapp.RequestHandler):
    def get(self):
		#url parameter
		urlParam = ""
		urlParamName = 'url'
		if (urlParamName in self.request.params):
			urlParam = urllib.quote(self.request.params[urlParamName])
	
		#topic parameter
		topicParam = ""
		topicParamName = 'topic'
		if (topicParamName in self.request.params):
			topicParam = self.request.params[topicParamName]
		
		#language parameter
		languageParam = "en"
		languageParamName = 'lan'
		if (languageParamName in self.request.params):
			languageParam = self.request.params[languageParamName]	
		
		#localization
		shareThisLabel = 'Share Health Topic'
		if (languageParam == 'es'):
			shareThisLabel = 'Compartir Informacion de Salud'
		
		#localization
		closeWindowLabel = 'Cancel'
		if (languageParam == 'es'):
			closeWindowLabel = 'Cerrar Ventana'	
			
		template_values = { 'sharethis_label': shareThisLabel,
							'language': languageParam, 
							'topic_text': topicParam, 
							'topic_url': urlParam,
							'closewindow_label': closeWindowLabel
						   }
		path = os.path.join(os.path.dirname(__file__), 'templates')
		path = os.path.join(path, 'sharethis.html')
		self.response.out.write(template.render(path, template_values))