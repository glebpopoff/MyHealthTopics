#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Hospital Info Health Guide RESTful API Service
# The hospital data was downloaded in CSV format from http://www.medicare.gov/download/downloaddb.asp
# and uploaded using AppEngine data loaders into persistance storage
#
# URL: /api/hospital-search/geopt/34.744963,-87.6754578/format/json
# The service returns hospitals by lat/lon
#

import datetime
import time
import os
import csv
import email.utils
import calendar
import logging
from UserString import MutableString
import urllib
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from models.HospitalModels import HospitalInfo
import Formatter
import AppConfig
import UtilLib
import math
import string
from geo import geobox2

# class definition
class GetHospitalsByGeoPtHandler(webapp.RequestHandler):
	#controller main entry		
	def get(self,geopt=None,format='json'):
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		#validate lat/lon
		if (not geopt or geopt == ''):
			self.response.out.write(Formatter.error(format, 'invalid GeoPoint'))
			return
	
		geoData = urllib.unquote(geopt).split(',')
		if (geoData and len(geoData) == 2):
			lon = geoData[1]
			lat = geoData[0]
			logging.debug("GPS Coordinates: %s,%s" % (lat,lon))
			gb = geobox2.Geobox(lat, lon)
			#scope 100 miles
			box = gb.search_geobox(100)
			query = HospitalInfo.all().filter("geoboxes IN", [box])
			#get 100 records
			results = query.fetch(100)
			db_recs = {}
			for result in results:
				distance = UtilLib.getEarthDistance(lat, lon, result.location.lat, result.location.lon)
				if (distance and distance > 0):
					db_recs[distance] = result
			
			returnData = MutableString()
			returnData = ''
					
			#output this badboy
			if (db_recs and len(db_recs) > 0):
				for key in sorted(db_recs.iterkeys()):
					p = db_recs[key]
					if (format == 'json'):
						startTag = '{'
						endTag = '},'
						distance = Formatter.data(format, 'distance', '%s %s' % (str(math.ceil(key)), "mi"))[:-1]#'%.2g %s' % (key, "mi"))[:-1]
					else:
						startTag = '<record>'
						endTag = '</record>'
						distance = Formatter.data(format, 'distance', '%s %s' % (str(math.ceil(key)), "mi"))
					#build the string	
					returnData = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (returnData,startTag,
																Formatter.data(format, 'hospital_id', p.hospital_id),
																Formatter.data(format, 'name', p.name.replace('&', '&amp;')),
																Formatter.data(format, 'address', p.address.replace('&', '&amp;')),
																Formatter.data(format, 'city', p.city),
																Formatter.data(format, 'state', p.state),
																Formatter.data(format, 'zip_code', p.zip_code),
																Formatter.data(format, 'county', p.county.replace('&', '&amp;')),
																Formatter.data(format, 'phone', p.phone),
																Formatter.data(format, 'hospital_type', p.hospital_type.replace('&', '&amp;')),
																Formatter.data(format, 'hospital_owner', p.hospital_owner.replace('&', '&amp;')),
																Formatter.data(format, 'emergency_service', p.emergency_service),
																Formatter.data(format, 'geo_location', p.location),
																distance,
																endTag
																)
																 
			
			#output to the browser
			self.response.out.write(Formatter.dataWrapper(format, returnData))
		else:
			self.response.out.write(Formatter.error(format, 'Unable to retrieve lat/lon from received GeoPoint'))
			return