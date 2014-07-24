#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Data Translation API using Google Translate REST Service
# The translated data is returned in 
#
# Usage: 
# POST URL: /api/translate
# Params: 
#- data=data to translate
#- format=json|xml
#- language=language to translate to (e.g. es)
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
from models.HospitalModels import DialysisCenter
import urllib
import Formatter
import AppConfig
import UtilLib
from api import CharReplacementMap
from xml.sax.saxutils import escape

#class definition
class GetTranslateHandler(webapp.RequestHandler):
	
	#Translate Api has a limit on length of text(4500 characters) that can be translated at once
	def getSplits(self,text,splitLength=4500): 
		return (text[index:index+splitLength] for index in xrange(0,len(text),splitLength))

	
	#controller main entry		
	def post(self):
		#set content-type		
		format = "json"
		formatParamName = "format"
		if (formatParamName in self.request.params):
			format = self.request.params[formatParamName]
		
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		#get content
		textToTranslate = ""
		textParamName = "data"
		if (textParamName in self.request.params):
			textToTranslate = self.request.params[textParamName]
		
		if (textToTranslate == None or textToTranslate == ''):
			logging.error('GetTranslateHandler: invalid parameters')
			self.response.out.write(Formatter.error(format, 'Invalid parameters'))
			return
		
		#strip tags?
		stripTagsParam = "striphtml"
		if (stripTagsParam in self.request.params):
			if (self.request.params[stripTagsParam] == 'true'):
				textToTranslate = CharReplacementMap.remove_html_tags(textToTranslate)
		
		#language
		toLanguage = "es"
		lanParam = "language"
		if (textParamName in self.request.params):
			toLanguage = self.request.params[lanParam]
		
		#auto-detect language (blank)
		sourceLanguage = ''
		params = ({'langpair': '%s|%s' % (sourceLanguage, toLanguage), 'v': '1.0' })
		returnData = MutableString()
		translatedText = '' 
		for textToTranslate in self.getSplits(textToTranslate): 
			params['q'] = textToTranslate 
			resp = simplejson.load(urllib.urlopen('%s' % (AppConfig.googleTranslateAPIURL), data = urllib.urlencode(params))) 
			try:
				translatedText += resp['responseData']['translatedText']
			except Exception, e:
				logging.error('GetTranslateHandler: error(s) translating data: %s' % e)
				self.response.out.write(Formatter.error(format, 'Exception: %s' % (e)))
				return

		#format the text
		if (translatedText):
			if (format == 'json'):
				#cleanup
				translatedText = re.sub("\"", "\\\"", translatedText)
				translatedText = re.sub("\n", "", translatedText)
				translatedText = re.sub("\t", " ", translatedText)
				
				if (len(translatedText) > 0):
					translatedText = Formatter.data(format, 'data', escape(translatedText))[:-1]
					self.response.out.write("{%s}" % translatedText)
				else:
					logging.error('GetTranslateHandler: unable to translate data')
					self.response.out.write(Formatter.error(format, 'Unable to translate data'))
			else:
				startTag = '<record>'
				endTag = '</record>'		
				if (len(translatedText) > 0):
					translatedText = Formatter.data(format, 'data', escape(translatedText))
					self.response.out.write(Formatter.dataWrapper(format, translatedText))
				else:
					logging.error('GetTranslateHandler: unable to translate data')
					self.response.out.write(Formatter.error(format, 'Unable to translate data'))
			
		else:
			logging.error('GetTranslateHandler: unable to translate data')
			self.response.out.write(Formatter.error(format, 'Unable to translate data'))
			return