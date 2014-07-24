#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Utility Class
#

from django.utils import simplejson
import logging
from google.appengine.api import urlfetch
import math

# Radius of the earth in miles.
RADIUS = 3963.1676

def getEarthDistance(lat1, lon1, lat2, lon2):
  lat1, lon1 = math.radians(float(lat1)), math.radians(float(lon1))
  lat2, lon2 = math.radians(float(lat2)), math.radians(float(lon2))
  return RADIUS * math.acos(math.sin(lat1) * math.sin(lat2) +
      math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1))

#call reverse geocoding service and get json data
def reverseGeo(urlStr):
	try:
		logging.debug('reverseGeo: %s' % urlStr)
		result = urlfetch.fetch(url=urlStr, deadline=30)
		if result.status_code == 200:
			jsonData = simplejson.loads(result.content)
		else:
			logging.error('reverseGeo: unable to translate Address into GPS coordinates...Attempt #1')
			return
	except Exception, ex:
		logging.error('reverseGeo: unable to translate Address into GPS coordinates...Attempt #1. Exception: %s' % ex)
		#lets try to resubmit the request
		try:
			result = urlfetch.fetch(url=urlStr, deadline=30)
			if result.status_code == 200:
				jsonData = simplejson.loads(result.content)
			else:
				logging.error('reverseGeo: unable to translate Address into GPS coordinates...Attempt #2')
				return
		except Exception, ex2:
			logging.error('reverseGeo: unable to translate Address into GPS coordinates...Attempt #2. Exception: %s' % ex2)
			return
			
	return jsonData