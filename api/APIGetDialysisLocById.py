#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Dialysis Center Info Health Guide RESTful API Service
# The dialysis data was downloaded in CSV format from http://www.medicare.gov/download/downloaddb.asp
# and uploaded using AppEngine data loaders into persistance storage
#
# URL: /api/dialysis-center-info/id/1004/format/json
# The service returns a single dialysis center record by ID
#

import datetime
import time
import os
import csv
import email.utils
import calendar
import logging
from UserString import MutableString
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from models.HospitalModels import DialysisCenter
import Formatter
import string
import UtilLib
import AppConfig

# class definitino
class GetDialysisLocByIdHandler(webapp.RequestHandler):
	#controller entry point
	def get(self,id=None,format='json'):	
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
			
		#validate id
		if (not id or id == ''):
			self.response.out.write(Formatter.error(format, 'invalid id'))
			return
		
		#get the record
		q = db.GqlQuery("SELECT * FROM DialysisCenter WHERE location_id = :1", id)
		
		#call storage and build up result string
		results = q.fetch(1)
		returnData = MutableString()
		returnData = ''
		for p in results:
		    if (p):
				returnData = "%s%s%s%s%s%s%s%s%s%s%s%s%s" % (Formatter.data(format, 'location_id', p.location_id),
															Formatter.data(format, 'name', p.name.replace('&', '&amp;')),
															Formatter.data(format, 'address', p.address.replace('&', '&amp;')),
															Formatter.data(format, 'address2', p.address2.replace('&', '&amp;')),
															Formatter.data(format, 'city', p.city),
															Formatter.data(format, 'state', p.state),
															Formatter.data(format, 'zip_code', p.zip_code),
															Formatter.data(format, 'owner', p.owner),
															Formatter.data(format, 'phone', p.phone),
															Formatter.data(format, 'in_center_hemo', p.hemo.replace('&', '&amp;')),
															Formatter.data(format, 'in_center_pd', p.pd.replace('&', '&amp;')),
															Formatter.data(format, 'geo_location', p.location),
															Formatter.data(format, 'geo_box', string.join(p.geoboxes, ","))
															)
	
		#output to the browser
		if (format == 'json'):
			self.response.out.write('{')
			self.response.out.write(returnData[:-1])
			self.response.out.write('}')
		else:
			self.response.out.write('<?xml version="1.0"?>')
			self.response.out.write('<root>')
			self.response.out.write(returnData)
			self.response.out.write('</root>')