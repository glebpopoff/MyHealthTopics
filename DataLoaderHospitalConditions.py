#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Data Loader Controller Router
# Takes data from the hospital address file, computes geobox values (proximity search)  then uploads to google BT storage
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

class DataLoaderHospConditions(Loader):
	
	def trim_str(self,s):
		return s.strip().decode('utf-8')
	
	dummy = lambda x: None
	
	def __init__(self):
		Loader.__init__(self, 'HospitalCondition',
		                                   [('hospital_id', self.trim_str),
		                                    ('condition', self.trim_str),
											('score', self.trim_str)
		                                   ])

loaders = [DataLoaderHospConditions]