#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Main controller for the Desktop Version of the app
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
from google.appengine.ext import db
from google.appengine.ext.webapp import util
import AppConfig
from models.HospitalModels import NewsCache
from UserString import MutableString
from api import APIUtils
from api import CharReplacementMap

#main controller for touch supported devices
class DesktopAppHandler(webapp.RequestHandler):
	"""
	def __init__(self):
		try:
			self.__init__
		except Exception, ex:
			pass
	"""			
	def get(self):
		isMobile = False
		ua = self.request.user_agent
		b = AppConfig.mobileDetectionB.search(ua)
		v = AppConfig.mobileDetectionV.search(ua[0:4])
		if (b or v):
			isMobile = True
			#ok, it's mobile see if it's android tablet
			if ("android" in ua.lower() and not "mobile" in ua.lower()):
				isMobile = False
			
		returnData = MutableString()
		returnData = ''
		healthNewsLabel = 'Health News'
		searchButtonLabel = ' Search '
		languageParamName = "lan"
		aboutUsLabel = ' About '
		keywordICD9SwitchKeywordLabel = 'Keyword'
		languageSelectionEnglish = "checked='checked'"
		languageSelectionSpanish = ""
		language = "en"
		moreNewsLabel = 'More News'
		if (languageParamName in self.request.params):
			language = self.request.params[languageParamName]
		
		now = datetime.datetime.now()
		newsDate = now.strftime("%Y-%m-%d")
		newsRec_k = db.Key.from_path('NewsCache', '%s_%s' % (newsDate,language))
		hasCacheData = False
		httpResponse = None	
		
		dbRec = db.get(newsRec_k)
		if (dbRec != None):
			hasCacheData = True
		
		if (language == 'es'):
			aboutUsLabel = ' Sobre Nosotros '
			moreNewsLabel = 'Ver Mas'
			searchButtonLabel = ' Busqueda '
			healthNewsLabel = 'Noticias de Salud'
			languageSelectionSpanish = "checked='checked'"
			languageSelectionEnglish = ""
			keywordICD9SwitchKeywordLabel = 'Palabra Clave'
			if (not hasCacheData):
				httpResponse = urllib.urlopen(AppConfig.medlinePlusHealthNewsSpanishURL)
		else:
			if (not hasCacheData):
				httpResponse = urllib.urlopen(AppConfig.medlinePlusHealthNewsEnglishURL)

		xmlString = ''
		dom = None
		if (not hasCacheData and httpResponse):
			xmlString = httpResponse.read()
			if (xmlString):
				dom = minidom.parseString(xmlString)
				#save record
				dbRec = NewsCache(key_name='%s_%s' % (newsDate,language))
				dbRec.xml = xmlString.decode('utf-8')
				dbRec.lan = language
				dbRec.put()
		else:
			xmlString = dbRec.xml
			dom = minidom.parseString(xmlString.encode('utf-8'))
		""""
		
		personRec = db.get(person_k)
		if (personRec != None):
		#self.response.out.write(personRec.milesno)
		logging.debug('save: updating existing instnace')
		else :
		
		logging.debug('save: creating new instnace')

		
		if ()
		"""
		
		rssTitle = MutableString()
		rssDescription = MutableString()
		rssURL = MutableString()
		healthNewsContainerTotal = []
		container = {}
		for node in dom.getElementsByTagName('item'):
			for item_node in node.childNodes:
				rssTitle = ''
				rssDescription = ''
				rssURL = ''
				
				#item title
				if (item_node.nodeName == "title"):
					for text_node in item_node.childNodes:
						if (text_node.nodeType == node.TEXT_NODE):
							rssTitle += text_node.nodeValue
				#description
				if (item_node.nodeName == "description"):
					for text_node in item_node.childNodes:
						rssDescription += text_node.nodeValue
				#link to URL
				if (item_node.nodeName == "link"):
					for text_node in item_node.childNodes:
						rssURL += text_node.nodeValue

				rssTitle = re.sub("\n", "", rssTitle)
				rssTitle = re.sub("\"", "\\\"", rssTitle)
				rssDescription = re.sub("\"", "\\\"", rssDescription)
				rssDescription = re.sub("\n", "", rssDescription)
				rssDescription = re.sub("\t", " ", rssDescription)
				rssDescription = re.sub("\r", "", rssDescription)							
				rssDescription = CharReplacementMap.remove_html_tags(rssDescription)
				
				if (len(rssURL) > 0):
					container['url'] = rssURL
					
				if (len(rssTitle) > 0):
					container['title'] = rssTitle

				if (len(rssDescription) > 0 ):
					container['description'] = rssDescription
				
				if (container.has_key('url') and container.has_key('title') and container.has_key('description')):
					healthNewsContainerTotal.append(container)
					container = {}
		
		counter = 0
		for healthRecord in healthNewsContainerTotal:
			if (counter < 3):
				returnData += '<li data-theme="c" class="ui-btn ui-btn-icon-right ui-li ui-btn-up-c"><div class="ui-btn-inner ui-li"><div class="ui-btn-text"><a href="' + healthRecord['url'] + '" class="ui-link-inherit"><h3 class="ui-li-heading">' + healthRecord['title'] + '</h3><p class="ui-li-desc">' + healthRecord['description'] + '</p></a></div><span class="ui-icon ui-icon-arrow-r ui-icon-shadow"></span></div></li>'
				counter = counter + 1
			
		template_values = {'healthnews': returnData, 
						   'language_selection_english': languageSelectionEnglish, 
						   'language_selection_spanish': languageSelectionSpanish, 
						   'language': language, 
						   'is_mobile': isMobile,
						   'aboutus_label': aboutUsLabel,
						   'more_news_label': moreNewsLabel,
						   'healthnewslabel': healthNewsLabel, 
						   'keywordicd9switchlabel': keywordICD9SwitchKeywordLabel,
						   'search_button_label': searchButtonLabel
						  }
		path = os.path.join(os.path.dirname(__file__), 'templates')
		path = os.path.join(path, 'desktop.html')
		self.response.out.write(template.render(path, template_values))