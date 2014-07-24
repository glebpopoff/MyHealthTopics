#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Results Page
#

import datetime
import time
import os
import email.utils
import calendar
import logging
from UserString import MutableString
from models.HospitalModels import HospitalInfo
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from xml.dom import minidom
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
import AppConfig
import urllib
import math
from geo import geobox2
import UtilLib
from api import APIUtils
import HealthTopicImageMap
from xml.sax.saxutils import unescape

#results page: /results?lan=en&keyword=asthma&zip=06032&type=icd9
class ResultsAppHandler(webapp.RequestHandler):

    #Translate Api has a limit on length of text(4500 characters) that can be translated at once
	def getSplits(self,text,splitLength=4500): 
		return (text[index:index+splitLength] for index in xrange(0,len(text),splitLength))

	#call google translate
	def translateData(self,toLanguage,sourceLanguage,textToTranslate):
		#auto-detect language (blank)
		params = ({'langpair': '%s|%s' % (sourceLanguage, toLanguage), 'v': '1.0' })
		translatedText = '' 
		for textToTranslate in self.getSplits(textToTranslate): 
			params['q'] = textToTranslate 
			resp = simplejson.load(urllib.urlopen('%s' % (AppConfig.googleTranslateAPIURL), data = urllib.urlencode(params))) 
			try:
				translatedText += resp['responseData']['translatedText']
			except Exception, e:
				logging.error('translateData: error(s) translating data: %s' % e)

		return translatedText

	#get hospital data from DB
	def getHospitalDBRecords(self,lat,lon):
		#get hospital data
		gb = geobox2.Geobox(lat, lon)
		box = gb.search_geobox(50)
		query = HospitalInfo.all().filter("geoboxes IN", [box])
		results = query.fetch(50)
		db_recs = {}
		for result in results:
			distance = UtilLib.getEarthDistance(lat, lon, result.location.lat, result.location.lon)
			if (distance and distance > 0):
				db_recs[distance] = result
		
		return db_recs
	
	#generate GoogleMaps JS from db records
	def getHospitalMapJS(self,db_recs):

		returnData = MutableString()
		returnData = ''

		counter = 0
		#output this badboy
		if (db_recs and len(db_recs) > 0):
			for key in sorted(db_recs.iterkeys()):
				if (counter < 15):
					p = db_recs[key]
					distance = '%s' % str(math.ceil(key))
					
					#format the phone
					formattedPhone = ''
					if (p.phone):
						if len(p.phone) > 3:
							formattedPhone = p.phone[-7:-4] + '-' + p.phone[-4:]
						if len(p.phone) > 7:
							formattedPhone = p.phone[:-10] + '(' + p.phone[-10:-7] + ') ' + p.phone[-7:-4] + '-' + p.phone[-4:]
					
					#build the string
					returnData += 'codeLatLon(%f, %f, "%s", "%s", "%s");\n' % (p.location.lat,
															p.location.lon,
															p.name.replace('&', '&amp;'),
															p.hospital_id,
															formattedPhone
															)
				counter = counter + 1
			return returnData
							
	#generate HTML from db records
	def getHospitalHTML(self,db_recs):
		
		returnData = MutableString()
		returnData = ''
		
		counter = 0
		#output this badboy
		if (db_recs and len(db_recs) > 0):
			for key in sorted(db_recs.iterkeys()):
				if (counter < 15):
					p = db_recs[key]
					distance = '%s' % str(math.ceil(key))
					
					#format the phone
					formattedPhone = ''
					if (p.phone):
						if len(p.phone) > 3:
							formattedPhone = p.phone[-7:-4] + '-' + p.phone[-4:]
						if len(p.phone) > 7:
							formattedPhone = p.phone[:-10] + '(' + p.phone[-10:-7] + ') ' + p.phone[-7:-4] + '-' + p.phone[-4:]

					#build the string
					returnData += '<li id="%s" style="cursor:pointer;"><h4 class="ui-li-heading"><a href="#">%s</a></h4><div class="ui-li-heading">%s<br />%s, %s %s<br />	%s<br /> </div>	<div class="ui-li-aside ui-li-heading">Distance: %s miles<br />Emergency Services: %s</div></li>' % (p.hospital_id,p.name.replace('&', '&amp;'), p.address.replace('&', '&amp;'), p.city, p.state, p.zip_code, formattedPhone, distance, p.emergency_service)
						
				counter = counter + 1
			return returnData
	
	#output to the browser
	def out(self, txt):
		self.response.out.write(txt)
	
	#get health topics by keyword
	def getTopicData(self,xml,lan='en'):
		if (xml):
			documentElms = xml.getElementsByTagName('document')
			if (documentElms):
				#grab two highest ranked content
				content1 = ''
				content2 = ''
				content3 = ''

				contentNode1 = documentElms[0]
				content1 = APIUtils.parseHealthTopicContent('json',contentNode1)

				if (len(documentElms) > 0):
					contentNode2 = documentElms[1]
					content2 = APIUtils.parseHealthTopicContent('json',contentNode2)

				if (len(documentElms) > 1):
					contentNode3 = documentElms[2]
					content3 = APIUtils.parseHealthTopicContent('json',contentNode3)

				returnData = "%s%s%s" % (content1, content2, content3)

				return returnData
			else:
				logging.error('unable to retrieve health topic content')
		else:
			logging.error('unable to retrieve health topic content')

	#get diagnosis data by ICD-9 code 
	def getDiagnosisICD9Data(self,xml):
		if (xml):
			documentElms = xml.getElementsByTagName('entry')
			if (documentElms):
				#grab two highest ranked content
				content1 = ''
				content2 = ''

				contentNode1 = documentElms[0]
				content1 = APIUtils.parseHealthDiagnosisICD9Content('json',contentNode1)

				if (len(documentElms) > 0):
					contentNode2 = documentElms[1]
					content2 = APIUtils.parseHealthDiagnosisICD9Content('json',contentNode2)

				returnData = "%s%s" % (content1, content2)
				return returnData		
			else:
				logging.error('unable to retrieve diagnosis content')
		else:
			logging.error('unable to retrieve diagnosis content')
			
	def get(self):
	
		#language parameter
		languageParam = "en"
		languageParamName = 'lan'
		if (languageParamName in self.request.params):
			languageParam = self.request.params[languageParamName]
	
		userLat = ""
		latParamName = 'lat'
		if (latParamName in self.request.params):
			userLat = self.request.params[latParamName]
	
		userLon = ""
		lonParamName = 'lon'
		if (lonParamName in self.request.params):
			userLon = self.request.params[lonParamName]
	
		#keyword parameter
		queryParam = "pain"
		keywordParameterName = 'keyword'
		if (keywordParameterName in self.request.params):
			queryParam = self.request.params[keywordParameterName]
	
		#zip parameter
		zipParam = ""
		zipParameterName = 'zip'
		if (zipParameterName in self.request.params):
			zipParam = self.request.params[zipParameterName]
		
		#type parameter
		typeParam = ""
		typeParameterName = 'type'
		if (typeParameterName in self.request.params):
			typeParam = self.request.params[typeParameterName]
	
		logging.debug('Get: Query=%s, Zip=%s, Language=%s, Type=%s' % (queryParam,zipParam,languageParam,typeParam))
		
		rpcTopic = None
		rpcDiagnosis = None
		diagnosisData = MutableString()
		topicData = MutableString()
		
		userState = 'CA'
		
		if (zipParam):
			#request to get lat,lon,and state based on a zipcode
			try:
				urlStr = 'http://maps.google.com/maps/geo?q=%s&output=json&sensor=true&key=%s' % (zipParam,AppConfig.googleMapsAPIKey)
				jsonData = UtilLib.reverseGeo(urlStr)	
				#lets see if have jsonData from reverse geocoding call
				if (jsonData):
					userLon = jsonData['Placemark'][0]['Point']['coordinates'][0]
					userLat = jsonData['Placemark'][0]['Point']['coordinates'][1]
					userState = jsonData['Placemark'][0]['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
				else:
					logging.error('Unable to retrieve geo information based on zipcode')
				
			except Exception,exTD1:
				logging.error('Errors getting geo data based on zipcode: %s' % exTD1)
		
		#async request to retrieve health topic or diagnosis data
		if (typeParam == 'keyword'):
			try:
				topicKeyword = queryParam
				#need to translate keyword to English
				if (languageParam == 'es'):
					topicKeyword = self.translateData('en','es',queryParam)
				
				url = '%s?db=healthTopics&term=%s' % (AppConfig.medlinePlusHealthTopicURL, topicKeyword)
				rpcTopic = urlfetch.create_rpc()
				urlfetch.make_fetch_call(rpcTopic, url)
			except Exception,exT:
				logging.error('Errors downloading health topic content: %s' % exT)
				#self.out(exT)
		else:
			try:
				#government webservice conversion (these guys aren't aware of international country codes)
				language = languageParam
				if (language == 'es'):
					language = 'sp'
				url = '%s&mainSearchCriteria.v.c=%s&informationRecipient.languageCode.c=%s' % (AppConfig.medlinePlusHealthDiagnosisICD9URL, queryParam, language)
				rpcDiagnosis = urlfetch.create_rpc()
				urlfetch.make_fetch_call(rpcDiagnosis, url)
			except Exception,exD:
				logging.error('Errors downloading health diagnosis content: %s' % exD)
				
		#get hospital data
		hospitalHTML = ''
		hospitalMapJS = ''
		if (userLat and userLon):
			hospitalDB = self.getHospitalDBRecords(userLat, userLon)
			hospitalHTML = self.getHospitalHTML(hospitalDB)
			hospitalMapJS = self.getHospitalMapJS(hospitalDB)
		
		#front-end variables
		healthDataLabel1 = ''
		healthDataLabel2 = ''
		healthDataLabel3 = ''
		healthDataSummary1 = ''
		healthDataSummary2 = ''
		healthDataSummary3 = ''
		
		#localization
		backButtonLabel = 'Back'
		topicInformationHeaderLabel = 'Health Topic Information'
		hospitalsTabLabel = 'Hospitals'
		clinicalTrialsTabLabel = 'Clinical Trials'
		healthUpdatesTabLabel = 'Health Updates'
		healthNewsTabLabel = 'Health News'
		shareThisLabel = 'Share This'
		aboutUsLabel = ' About '
		if (languageParam == 'es'):
			backButtonLabel = 'Volver'
			aboutUsLabel = ' Sobre Nosotros '
			topicInformationHeaderLabel = 'Informacion sobre la Salud'
			hospitalsTabLabel = 'Hospitales'
			clinicalTrialsTabLabel = 'Ensayos Clinicos'
			healthUpdatesTabLabel = 'Actualizaciones de salud'
			healthNewsTabLabel = 'Noticias de Salud'
			shareThisLabel = 'Compartir Este'
		
		#fetch ICD-9 diagnosis data
		diagnosisData = ''
		if (rpcDiagnosis):
			try:
			    resultDiagnosis = rpcDiagnosis.get_result()
			    if (resultDiagnosis and resultDiagnosis.status_code == 200):
					if (resultDiagnosis.content):
						diagnosisData = self.getDiagnosisICD9Data(minidom.parseString(resultDiagnosis.content))
					else:
						logging.error('unable to retrieve diagnosis content')
			except Exception,ex:
				logging.error('Errors getting diagnosis content: %s' % ex)
						
		#fetch health topic data
		topicData = ''
		if (rpcTopic):
			try:
			    resultTopic = rpcTopic.get_result()
			    if (resultTopic and resultTopic.status_code == 200):
					if (resultTopic.content):
						topicData = self.getTopicData(minidom.parseString(resultTopic.content),languageParam)
					else:
						logging.error('unable to retrieve health topic content')
			except Exception,ex:
				logging.error('Errors retrieving health topic content: %s' % ex)

		if (diagnosisData):
			try:
				#python is awesome. convert JSON string into Python container
				diagnosisContainer = simplejson.loads("[%s]" % diagnosisData[:-1])
				counter = 0
				for topic in diagnosisContainer:
					if (counter == 0):
						healthDataLabel1 = topic['title']
						healthDataSummary1 = unescape(topic['summary'])
					if (counter == 1):
						healthDataLabel2 = topic['title']
						healthDataSummary2 = unescape(topic['summary'])
					counter = counter + 1
				
			except Exception,ex:
				logging.error('Errors converting Diagnosis JSON string into Python Object: %s' % ex)

		if (topicData):
			try:
				#python is awesome. convert JSON string into Python container
				healthTopicContainer = simplejson.loads("[%s]" % topicData[:-1])
				counter = 0
				for topic in healthTopicContainer:
					if (counter == 0):
						healthDataLabel1 = topic['title']
						healthDataSummary1 = unescape(topic['summary'])
					if (counter == 1):
						healthDataLabel2 = topic['title']
						healthDataSummary2 = unescape(topic['summary'])
					if (counter == 2):
						healthDataLabel3 = topic['title']
						healthDataSummary3 = unescape(topic['summary'])
					counter = counter + 1
				
			except Exception,ex:
				logging.error('Errors converting Topic JSON string into Python Object: %s' % ex)
		
		
		#set default values
		if (not userLat):
			userLat = 37.777770
		if (not userLon):	
			 userLon = -122.423058
		if (not userState):
			userState = 'CA'
		
		doTranslateData = False
		if (languageParam == 'es'):
			doTranslateData = True
		
		#set django template vars		
		template_values = {
							'hospital_data_results':hospitalHTML, 
							'hospital_map_results':hospitalMapJS, 
						  	'user_lat': userLat, 
							'user_lon': userLon,
							'translate_data': doTranslateData,
							'aboutus_label': aboutUsLabel,
							'query_param': queryParam,
							'language_param': languageParam,
							'user_state': userState,
							'health_data_label1': healthDataLabel1,
							'url_encoded': urllib.quote('http://acsyshealthguide.appspot.com/results?lan=%s&keyword=%s&zip=%s&type=%s' % (languageParam, queryParam, zipParam, typeParam)),
							'health_main_topic_encoded': urllib.quote(healthDataLabel1),
							'health_data_summary1': healthDataSummary1,
							'health_data_label2': healthDataLabel2,
							'health_data_summary2': healthDataSummary2,
							'health_data_label3': healthDataLabel3,
							'health_data_summary3': healthDataSummary3,
							'health_topic_image': HealthTopicImageMap.get_health_topic_image(queryParam),
							'backbutton_label': backButtonLabel,
							'topicinformation_label': topicInformationHeaderLabel,
							'hospitalstab_label': hospitalsTabLabel,
							'clinicaltrialstab_label': clinicalTrialsTabLabel,
							'healthupdatestab_label': healthUpdatesTabLabel,
							'healthnewstab_label': healthNewsTabLabel,
							'sharethis_label': shareThisLabel
							
						  }
		path = os.path.join(os.path.dirname(__file__), 'templates')
		path = os.path.join(path, 'results.html')
		self.response.out.write(template.render(path, template_values))