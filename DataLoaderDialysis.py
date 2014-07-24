#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Data Loader Controller Router
# Takes data from the dialysis address file, computes geobox values (proximity search)  then uploads to google BT storage
#

import logging
import datetime
import os
import sys
import csv
from google.appengine.ext import db
from google.appengine.tools.bulkloader import Loader
sys.path.append('.')
from models import HospitalModels
from geo import geobox2

class DataLoaderDialysis(Loader):
	
	def lat_lon(self,s):
		lat, lon = [float(v) for v in s.split(',')]
		if (lat and lon):
			return db.GeoPt(lat, lon)
		else:
			return db.GeoPt(0, 0)
		
	def geo_box(self,s):
		lat, lon = [float(v) for v in s.split(',')]
		if (lat and lon):
			gb = geobox2.Geobox(lat, lon)
			return gb.storage_geoboxes()
		else:
			return ['0.000|0.000|0.000|0.000']
	
	def trim_str(self,s):
		return s.strip().decode('utf-8')
	
	dummy = lambda x: None
	
	def __init__(self):
		Loader.__init__(self, 'DialysisCenter',
		                                   [('location_id', self.trim_str),
		                                    ('name', self.trim_str),
		                                    ('address', self.trim_str),
											('address2', self.trim_str),
											('city', self.trim_str),
											('state', self.trim_str),
											('zip_code', self.trim_str),
											('phone', self.trim_str),
											('owner', self.trim_str),
											('hemo', self.trim_str),
											('pd', self.trim_str),
											('location_id_geo_ref', self.trim_str),
											('location', self.lat_lon),
											('geoboxes', self.geo_box),
		                                   ])
	
	def create_entity(self, values, key_name=None, parent=None):
		if (values and len(values) >= 13):
			values[12] = values[12] + ',' + values[13]
			#set the 16th column for geobox property
			values[13] = values[12]
		
		return super(DataLoaderDialysis, self).create_entity(values, key_name)

loaders = [DataLoaderDialysis]