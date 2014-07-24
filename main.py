#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Main App Controller Router
#

import datetime
import time
import os
import email.utils
import calendar
import logging
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from DesktopController import DesktopAppHandler
from api.APIGetHospitalsByZip import GetHospitalsByZipHandler
from api.APIGetHospitalsByCondition import GetHospitalsByConditionHandler
from api.APIGetHospitalsById import GetHospitalsByIdHandler
from api.APIGetHospitalsByGeoPt import GetHospitalsByGeoPtHandler
from api.APIGetHospitalsByCityState import GetHospitalsByCityStateHandler
from ResultsController import ResultsAppHandler
from GeoController import GeoCodeController
from APIController import APIHandler
from api.APIGetDialysisLocByZip import GetDialysisLocByZipHandler
from api.APIGetDialysisLocByCityState import GetDialysisLocByCityStateHandler
from api.APIGetDialysisLocByGeoPt import GetDialysisLocByGeoPtHandler
from api.APIGetDialysisLocById import GetDialysisLocByIdHandler
from api.APIHealthUpdates import GetHealthUpdatesHandler
from api.APIHealthNews import GetHealthNewsHandler
from api.APIHealthTopics import GetHealthTopicsHandler
from api.APIHealthDiagnosisICD9 import GetHealthDiagnosisICD9Handler
from api.APIDataTranslation import GetTranslateHandler
from api.APIClinicalTrials import GetClinicalTrialsHandler
from api.APIHealthMasterDataSet import GetHealthSuperDataSetHandler
from NewsController import NewsAppHandler
from ShareThisController import ShareThisAppHandler
from AboutController import AboutAppHandler

#application controllers
def main():
	application = webapp.WSGIApplication([('/', DesktopAppHandler),
										  (r'/api/healthsdataset/query/(.*)/zip/(.*)/lan/(en|es)/type/(keyword|icd9)/format/(json|xml)', GetHealthSuperDataSetHandler),
										  (r'/api/clinicaltrials/keyword/(.*)/state/(.*)/format/(json|xml)', GetClinicalTrialsHandler),
										  (r'/api/healthdata/code/(.*)/lan/(en|es)/format/(json|xml)', GetHealthDiagnosisICD9Handler),
										  (r'/api/healthdata/code/(.*)', GetHealthDiagnosisICD9Handler),
 										  (r'/api/healthdata/keyword/(.*)/format/(json|xml)', GetHealthTopicsHandler),
										  (r'/api/healthdata/keyword/(.*)', GetHealthTopicsHandler),
										  (r'/api/healthupdates/format/(json|xml)', GetHealthUpdatesHandler),
										  (r'/api/healthupdates', GetHealthUpdatesHandler),
										  (r'/api/translate', GetTranslateHandler),
										  (r'/api/healthnews/lan/(en|es)/format/(json|xml)', GetHealthNewsHandler),
										  (r'/api/healthnews', GetHealthNewsHandler),
										  (r'/api/hospital-search/zip/(.*)/format/(json|xml)', GetHospitalsByZipHandler),
										  (r'/api/hospital-search/condition/(.*)/format/(json|xml)', GetHospitalsByConditionHandler),
										  (r'/api/hospital-search/citystate/(.*)/format/(json|xml)', GetHospitalsByCityStateHandler),
										  (r'/api/hospital-search/geopt/(.*)/format/(json|xml)', GetHospitalsByGeoPtHandler),
										  (r'/api/hospital-info/id/(.*)/format/(json|xml)', GetHospitalsByIdHandler),
										  (r'/api/dialysis-center-search/zip/(.*)/format/(json|xml)', GetDialysisLocByZipHandler),
										  (r'/api/dialysis-center-search/citystate/(.*)/format/(json|xml)', GetDialysisLocByCityStateHandler),
										  (r'/api/dialysis-center-search/geopt/(.*)/format/(json|xml)', GetDialysisLocByGeoPtHandler),
										  (r'/api/dialysis-center-info/id/(.*)/format/(json|xml)', GetDialysisLocByIdHandler),
										  ('/api', APIHandler),
										  ('/api/', APIHandler),
										  ('/results', ResultsAppHandler),
										  ('/news', NewsAppHandler),
										  ('/about', AboutAppHandler),
										  ('/desktop', DesktopAppHandler),
										  ('/share', ShareThisAppHandler)
										],
                                         debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	try:
		main()
	except Exception, ex:
		print('Error(s) in main controller: %s' % ex)
		pass