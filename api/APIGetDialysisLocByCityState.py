#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Dialysis Center Info Health Guide RESTful API Service
# The dialysis data was downloaded in CSV format from http://www.medicare.gov/download/downloaddb.asp
# and uploaded using AppEngine data loaders into persistance storage
#
# URL: /api/dialysis-center-search/citystate/farmington%2Cct/format/json
# The service returns dialysis centers by city & state (e.g. farmington,ct)
#

import datetime
import time
import os
import csv
import email.utils
import calendar
import logging
from UserString import MutableString
from google.appengine.api import urlfetch
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from models.HospitalModels import DialysisCenter
import Formatter
import AppConfig
import UtilLib
import math
import string
from geo import geobox2

#class definition
class GetDialysisLocByCityStateHandler(webapp.RequestHandler):
	#controller main entry		
	def get(self,citystate=None,format='json'):
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		#validate zip
		if (not citystate or citystate == ''):
			self.response.out.write(Formatter.error(format, 'invalid city state'))
			return
	
		#get lat/lon from city&state
		urlStr = 'http://maps.google.com/maps/geo?q=%s&output=json&sensor=true&key=%s' % (citystate,AppConfig.googleMapsAPIKey)
		jsonData = UtilLib.reverseGeo(urlStr)	
		#lets see if have jsonData from reverse geocoding call
		if (jsonData):
			lon = jsonData['Placemark'][0]['Point']['coordinates'][0]
			lat = jsonData['Placemark'][0]['Point']['coordinates'][1]
			logging.debug("GPS Coordinates: %s,%s" % (lat,lon))
			gb = geobox2.Geobox(lat, lon)
			#scope 100 miles
			box = gb.search_geobox(100)
			query = DialysisCenter.all().filter("geoboxes IN", [box])
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
																Formatter.data(format, 'location_id', p.location_id),
																Formatter.data(format, 'name', p.name.replace('&', '&amp;')),
																Formatter.data(format, 'address', p.address.replace('&', '&amp;')),
																Formatter.data(format, 'address2', p.address2.replace('&', '&amp;')),
																Formatter.data(format, 'city', p.city),
																Formatter.data(format, 'state', p.state),
																Formatter.data(format, 'zip_code', p.zip_code),
																Formatter.data(format, 'owner', p.owner.replace('&', '&amp;')),
																Formatter.data(format, 'phone', p.phone),
																Formatter.data(format, 'in_center_hemo', p.hemo.replace('&', '&amp;')),
																Formatter.data(format, 'in_center_pd', p.pd.replace('&', '&amp;')),
																Formatter.data(format, 'geo_location', p.location),
																distance,
																endTag
																)
																 
			
			#output to the browser
			self.response.out.write(Formatter.dataWrapper(format, returnData))
		else:
			self.response.out.write(Formatter.error(format, 'Unable to perform geocoding'))
			return