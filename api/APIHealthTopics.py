#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Health Topics RESTful API Service
# The health topics data is retrieved from the MedlinePlus service based on a keyword: 
# http://wsearch.nlm.nih.gov/ws/query?db=healthTopics&term=[keyword]
#
# URL: /api/healthdata/keyword/[keyword]/format/json
# Example (asthma): /api/healthdata/keyword/asthma/format/json
# Make sure keyword is URL-encoded
#

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
from api import APIUtils

# class definition
class GetHealthTopicsHandler(webapp.RequestHandler):
	#controller main entry		
	def get(self,keyword,format='json'):
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		returnData = MutableString()
		try:
			#get XML from the service
			xml = minidom.parse(urllib.urlopen('%s?db=healthTopics&term=%s' % (AppConfig.medlinePlusHealthTopicURL, keyword)))
			
			if (xml):
				documentElms = xml.getElementsByTagName('document')
				if (documentElms):
					#grab two highest ranked content
					content1 = ''
					content2 = ''
					content3 = ''
					
					contentNode1 = documentElms[0]
					content1 = APIUtils.parseHealthTopicContent(format,contentNode1)
					
					if (len(documentElms) > 1):
						contentNode2 = documentElms[1]
						content2 = APIUtils.parseHealthTopicContent(format,contentNode2)
					
					if (len(documentElms) > 2):
						contentNode3 = documentElms[2]
						content3 = APIUtils.parseHealthTopicContent(format,contentNode3)
					
					returnData = "%s%s%s" % (content1, content2, content3)
							
				else:
					logging.error('unable to retrieve content')
					self.response.out.write(Formatter.error(format, 'No results'))
					return
			else:
				logging.error('unable to retrieve content')
				self.response.out.write(Formatter.error(format, 'Unable to retrieve content from provider'))
				return
					
		except Exception, e:
			logging.error('GetHealthTopicsHandler: unable to get health topics or parse XML: %s' % e)
			self.response.out.write(Formatter.error(format, 'Exception: %s' % (e)))
			return
		
		#output to the browser
		self.response.out.write(Formatter.dataWrapper(format, returnData))