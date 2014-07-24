#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Removes Entities from big table. Do NOT push to PROD.
#

import datetime
import time
import os
import email.utils
import calendar
import logging
from UserString import MutableString
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from models.HospitalModels import HospitalInfo

class CleanupAppHandler(webapp.RequestHandler):
    def get(self):
		#db.delete(HospitalInfo.all())
		self.response.out.write('Done')