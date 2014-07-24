#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Health Updates RESTful API Service
# The health updates are retrieved from FDA's RSS service: http://www.fda.gov/AboutFDA/ContactFDA/StayInformed/RSSFeeds/Consumers/rss.xml
#
# URL: /api/healthupdates/format/json
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
from xml.dom import minidom
import urllib

# class definition
class GetHealthUpdatesHandler(webapp.RequestHandler):
	#controller main entry		
	def get(self,format='json'):
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		returnData = MutableString()
		returnData = ''
		dom = minidom.parse(urllib.urlopen(AppConfig.fdaHealthUpdatesURL))
		rssTitle = MutableString()
		rssDescription = MutableString()
		rssURL = MutableString()
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
						if (text_node.nodeType == node.TEXT_NODE):
							rssDescription += text_node.nodeValue
				#link to URL
				if (item_node.nodeName == "link"):
					for text_node in item_node.childNodes:
						if (text_node.nodeType == node.TEXT_NODE):
							rssURL += text_node.nodeValue
				
				if (format == 'json'):
					startTag = '{'
					endTag = '},'
					
					#cleanup
					rssTitle = re.sub("\n", "", rssTitle)
					rssTitle = re.sub("\"", "\\\"", rssTitle)
					rssDescription = re.sub("\"", "\\\"", rssDescription)
					rssDescription = re.sub("\n", "", rssDescription)
					rssDescription = re.sub("\t", " ", rssDescription)
					rssDescription = re.sub("\r", "", rssDescription)
					
					if (len(rssURL) > 0):
						rssURL = Formatter.data(format, 'url', rssURL)[:-1]
				else:
					startTag = '<record>'
					endTag = '</record>'		
					if (len(rssURL) > 0):
						rssURL = Formatter.data(format, 'url', rssURL)								
				
				if (len(rssTitle) > 0):
					returnData += startTag + Formatter.data(format, 'title', rssTitle)
					
				if (len(rssDescription) > 0):
					returnData += Formatter.data(format, 'description', rssDescription)
					
				if (len(rssURL) > 0):
					returnData += rssURL + endTag
					
		#output to the browser
		self.response.out.write(Formatter.dataWrapper(format, returnData))