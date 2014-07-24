#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# A location-aware model for hospital data
# HospitalGeoInfo uses GeoModel library (geo folder)
# HospitalGeoInfo: 7/6/11: Couldn't get it to work so for now this lib has been abandoned
#

import logging
from google.appengine.ext import db
from geo import geobox2
import math
#from geo.geomodel import GeoModel

class NewsCache(db.Model):
	record_date = db.DateTimeProperty(auto_now_add=True)	
	xml = db.TextProperty()
	lan = db.StringProperty()#multiline=True

class HospitalGeoBox(db.Model):
	hospital_id = db.StringProperty()
	geoboxes = db.StringListProperty()
	datecreated = db.DateTimeProperty(auto_now_add=True)	
	location = db.GeoPtProperty()

class HospitalCondition(db.Model):
	hospital_id = db.StringProperty()
	condition = db.StringProperty()
	score = db.StringProperty()
	datecreated = db.DateTimeProperty(auto_now_add=True)	

class DialysisCenter(db.Model):
	location_id = db.StringProperty()
	name = db.StringProperty()
	address = db.StringProperty()
	address2 = db.StringProperty()
	city = db.StringProperty()
	state = db.StringProperty()
	zip_code = db.StringProperty()
	phone = db.StringProperty()
	owner = db.StringProperty()
	hemo = db.StringProperty()
	pd = db.StringProperty()
	location_id_geo_ref = db.StringProperty()
	geoboxes = db.StringListProperty()
	location = db.GeoPtProperty()
	datecreated = db.DateTimeProperty(auto_now_add=True)

class HospitalInfo(db.Model):
	hospital_id = db.StringProperty()
	name = db.StringProperty()
	address = db.StringProperty()
	address2 = db.StringProperty()
	address3 = db.StringProperty()
	city = db.StringProperty()
	state = db.StringProperty()
	zip_code = db.StringProperty()
	county = db.StringProperty()
	phone = db.StringProperty()
	hospital_type = db.StringProperty()
	hospital_owner = db.StringProperty()
	emergency_service = db.StringProperty()
	hospital_id_geo_ref = db.StringProperty()
	geoboxes = db.StringListProperty()
	location = db.GeoPtProperty()
	datecreated = db.DateTimeProperty(auto_now_add=True)	
	
	"""
	@classmethod
	def query(cls, system, lat, lon, inbound, max_results, min_params):  
		found_stops = {}
		# Do concentric queries until the max number of results is reached.
		# Use only the first three geoboxes for search to reduce query overhead.
		for params in GEOBOX_CONFIGS[:3]:
			if len(found_stops) >= max_results:
				break
			if params < min_params:
				break

		resolution, slice, unused = params
		box = geobox.compute(lat, lon, resolution, slice)
		logging.debug("Searching for box=%s at resolution=%s, slice=%s", box, resolution, slice)
		query = cls.all()
		query.filter("geoboxes =", box)
		results = query.fetch(50)
		logging.debug("Found %d results", len(results))

		# De-dupe results.
		for result in results:
			if result.hospital_id not in found_stops:
				found_stops[result.hospital_id] = result

		# Now compute distances and sort by distance.
		stops_by_distance = []
		for stop in found_stops.itervalues():
			distance = _earth_distance(lat, lon, stop.location.lat, stop.location.lon)
			stops_by_distance.append((distance, stop))
		stops_by_distance.sort()
		return stops_by_distance[:max_results]
		"""
"""
#not being used for now
class HospitalGeoInfo(GeoModel):
	hospital_id = db.StringProperty()
	name = db.StringProperty()
	address = db.StringProperty()
	city = db.StringProperty()
	state = db.StringProperty()
	zip_code = db.IntegerProperty()
	county = db.StringProperty()
	phone = db.StringProperty()
	hospital_type = db.StringProperty()
	hospital_owner = db.StringProperty()
	emergency_service = db.StringProperty()
	datecreated = db.DateTimeProperty(auto_now_add=True)
	
	def _get_latitude(self):
		return self.location.lat if self.location else None

	def _set_latitude(self, lat):
		if not self.location:
			self.location = db.GeoPt()
		self.location.lat = lat

	latitude = property(_get_latitude, _set_latitude)

	def _get_longitude(self):
		return self.location.lon if self.location else None

	def _set_longitude(self, lon):
		if not self.location:
			self.location = db.GeoPt()
		self.location.lon = lon

	longitude = property(_get_longitude, _set_longitude)
"""