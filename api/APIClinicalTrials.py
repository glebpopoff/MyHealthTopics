#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Clinical Trials Health Guide RESTful API Service
# The clinical trials data is retrieved from the clinicaltrials.gov service: 
# http://clinicaltrials.gov/ct2/results?displayxml=true&term=[keyword]&state1=[countrystate]
#
# URL: /api/clinicaltrials/keyword/(.*)/state/(.*)/format/(json|xml)
# Example (asthma connecticut xml results): /api/clinicaltrials/keyword/asthma/state/CT/format/xml
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
class GetClinicalTrialsHandler(webapp.RequestHandler):
	#controller main entry		
	def get(self,keyword, state, format='json'):
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		returnData = MutableString()
		returnData = ''
		try:
			#get XML from the service
			state = "%s%s" % ("NA%3AUS%3A", state)
			xml = minidom.parse(urllib.urlopen('%s&term=%s&state1=%s' % (AppConfig.clinicalTrialsAPIURL, keyword, state.upper())))
			if (xml):
				documentElms = xml.getElementsByTagName('clinical_study')
				if (documentElms):
					for docNode in documentElms:
						content = APIUtils.parseClinicalTrialsContent(format,docNode)
						returnData += content
							
				else:
					logging.error('unable to retrieve content')
					self.response.out.write(Formatter.error(format, 'No results'))
					return
			else:
				logging.error('unable to retrieve content')
				self.response.out.write(Formatter.error(format, 'Unable to retrieve content from provider'))
				return
					
		except Exception, e:
			logging.error('GetClinicalTrialsHandler: unable to get health topics or parse XML: %s' % e)
			self.response.out.write(Formatter.error(format, 'Exception: %s' % (e)))
			return
		
		#output to the browser
		self.response.out.write(Formatter.dataWrapper(format, returnData))