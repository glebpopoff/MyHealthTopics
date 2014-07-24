#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Health Diagnosis RESTful API Service
# The health diagnosis data is retrieved from the MedlinePlus service based on the ICD-9 code: 
# http://apps.nlm.nih.gov/medlineplus/services/mpconnect_service.cfm?mainSearchCriteria.v.cs=2.16.840.1.113883.6.103&mainSearchCriteria.v.c=[code]&informationRecipient.languageCode.c=[language]
#
# URL: /api/healthdata/code/(.*)/lan/(en|es)/format/(json|xml)
# Example (250.33 english xml results): /api/healthdata/code/250.33/lan/en/format/xml
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
class GetHealthDiagnosisICD9Handler(webapp.RequestHandler):
	#controller main entry		
	def get(self,code, lan = 'en', format='json'):
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		returnData = MutableString()
		try:
			#webservice conversion
			if (lan == 'es'):
				lan = 'sp'
			
			#get XML from the service
			xml = minidom.parse(urllib.urlopen('%s&mainSearchCriteria.v.c=%s&informationRecipient.languageCode.c=%s' % (AppConfig.medlinePlusHealthDiagnosisICD9URL, code, lan)))
			
			if (xml):
				documentElms = xml.getElementsByTagName('entry')
				if (documentElms):
					#grab two highest ranked content
					content1 = ''
					content2 = ''
					
					contentNode1 = documentElms[0]
					content1 = APIUtils.parseHealthDiagnosisICD9Content(format,contentNode1)
					
					if (len(documentElms) > 0):
						contentNode2 = documentElms[1]
						content2 = APIUtils.parseHealthDiagnosisICD9Content(format,contentNode2)
					
					returnData = "%s%s" % (content1, content2)
							
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