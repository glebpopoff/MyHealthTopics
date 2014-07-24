#!/usr/bin/env python
#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011
# 
# Health Data Master DataSet RESTful API Service
# The API returns the following data in English or Spanish:
# - health topic or diagnosis data (based on a keyword or ICD-9 code)
# - hospitals in the nearby vicinity
#
# URL: /api/healthsdataset/query/(.*)/zip/(.*)/lan/(en|es)/type/(keyword|icd9)/format/(json|xml)
# Example (asthma for 06032 zipcode in english): 
# /api/healthsdataset/query/asthma/zip/06032/lan/en/type/keyword/format/xml
# Make sure query is URL-encoded
#

import re
import logging
from UserString import MutableString
from google.appengine.api import urlfetch
from django.utils import simplejson
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from models.HospitalModels import HospitalInfo
import Formatter
import AppConfig
import UtilLib
from geo import geobox2
from xml.dom import minidom
import urllib
import math
from api import APIUtils
from xml.sax.saxutils import unescape
from api import CharReplacementMap

# class definition
class GetHealthSuperDataSetHandler(webapp.RequestHandler):
	
	#Translate Api has a limit on length of text(4500 characters) that can be translated at once
	def getSplits(self,text,splitLength=4500): 
		return (text[index:index+splitLength] for index in xrange(0,len(text),splitLength))

	#call google translate
	def translateData(self,toLanguage,textToTranslate):
		#auto-detect language (blank)
		sourceLanguage = ''
		params = ({'langpair': '%s|%s' % (sourceLanguage, toLanguage), 'v': '1.0' })
		translatedText = '' 
		for textToTranslate in self.getSplits(textToTranslate): 
			params['q'] = textToTranslate 
			resp = simplejson.load(urllib.urlopen('%s' % (AppConfig.googleTranslateAPIURL), data = urllib.urlencode(params))) 
			try:
				translatedText += resp['responseData']['translatedText']
			except Exception, e:
				logging.error('translateTopic: error(s) translating data: %s' % e)

		return translatedText
	
	#get hospital data from DB
	def getHospitalData(self,lat,lon,format):
		#get hospital data
		gb = geobox2.Geobox(lat, lon)
		box = gb.search_geobox(100)
		query = HospitalInfo.all().filter("geoboxes IN", [box])
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
	
			if (format == 'json'):
				return returnData[:-1]
			else:
				return returnData
	
	#get health topics by keyword
	def getTopicData(self,xml,format,lan='en'):
		if (xml):
			documentElms = xml.getElementsByTagName('document')
			if (documentElms):
				#grab two highest ranked content
				content1 = ''
				content2 = ''
				content3 = ''
				
				contentNode1 = documentElms[0]
				content1 = APIUtils.parseHealthTopicContent(format,contentNode1)
				
				if (len(documentElms) > 1):
					contentNode2 = documentElms[1]
					content2 = APIUtils.parseHealthTopicContent(format,contentNode2)
				
				if (len(documentElms) > 2):
					contentNode3 = documentElms[2]
					content3 = APIUtils.parseHealthTopicContent(format,contentNode3)
				
				returnData = "%s%s%s" % (content1, content2, content3)
				
				"""
				Giving up for now....major pain in the butt to translate entire XML or JSON document
				
				#fun stuff: lets see if we need to translate
				#because we have three content records it's better to 
				#translate the entire document (json or xml) instead of individual content summaries
				translatedData = ''
				if (lan != 'en'):
					#prep data
					#if JSON, replace record definition with non-translatable text
					if (format == 'json'):
						returnData = re.sub("\"", "X59X", returnData)
					else:
						#get rid of the tags. Google Translate doesn't seem to like them
						returnData = returnData#CharReplacementMap.translate_tags_from_xml_record(returnData)
					
					translatedData = self.translateData(lan,returnData.encode("utf-8"))
					self.out(translatedData)
					
									
				if (translatedData):
					#cheesy search&replace - need a quick solution to fix JSON
					if (format == 'json'):
						translatedData = re.sub("X59X","\"", translatedData)
						translatedData = re.sub("\n", "", translatedData)
						translatedData = re.sub("\r", "", translatedData)
						translatedData = re.sub("\t", "", translatedData)
					else:
						translatedData = translatedData#CharReplacementMap.translate_tags_to_xml_record(translatedData)
					
					return translatedData
				"""	
				if (format == 'json'):
					return returnData[:-1]
				else:
					return returnData
			else:
				logging.error('unable to retrieve health topic content')
				return Formatter.data(format, 'error', 'No results')
		else:
			logging.error('unable to retrieve health topic content')
			return Formatter.data(format, 'error', 'Unable to retrieve content from provider')
	
	#get diagnosis data by ICD-9 code 
	def getDiagnosisICD9Data(self,xml,format):
		if (xml):
			documentElms = xml.getElementsByTagName('entry')
			if (documentElms):
				#grab two highest ranked content
				content1 = ''
				content2 = ''
				
				contentNode1 = documentElms[0]
				content1 = APIUtils.parseHealthDiagnosisICD9Content(format,contentNode1)
				
				if (len(documentElms) > 0):
					contentNode2 = documentElms[1]
					content2 = APIUtils.parseHealthDiagnosisICD9Content(format,contentNode2)
				
				returnData = "%s%s" % (content1, content2)
				if (format == 'json'):
					return returnData[:-1]
				else:
					return returnData		
			else:
				logging.error('unable to retrieve diagnosis content')
				return Formatter.data(format, 'error', 'No results')
		else:
			logging.error('unable to retrieve diagnosis content')
			return Formatter.data(format, 'error', 'Unable to retrieve content from provider')
	
	#print out
	def out(self,str):
		self.response.out.write(str)
		
	#controller main entry		
	def get(self,query,zip,lan='en',type='keyword',format='json'):
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		logging.debug('Get: Query=%s, Zip=%s, Language=%s, Type=%s, Format=%s' % (query,zip,lan,type,format))
		
		#data to output
		returnData = MutableString()
		returnData = ''
		
		rpcTopic = None
		rpcDiagnosis = None
		rpcClinicalTrials = None
		diagnosisData = MutableString()
		topicData = MutableString()
		clinicalTrialsData = MutableString()
		userState = None
		userLat = None
		userLon = None
		
		#request to get lat,lon,and state based on a zipcode
		try:
			urlStr = 'http://maps.google.com/maps/geo?q=%s&output=json&sensor=true&key=%s' % (zip,AppConfig.googleMapsAPIKey)
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
		if (type == 'keyword'):
			try:
				url = '%s?db=healthTopics&term=%s' % (AppConfig.medlinePlusHealthTopicURL, query)
				rpcTopic = urlfetch.create_rpc()
				urlfetch.make_fetch_call(rpcTopic, url)
			except Exception,exT:
				logging.error('Errors downloading health topic content: %s' % exT)
		else:
			try:
				#government webservice conversion (these guys aren't aware of international country codes)
				language = lan
				if (language == 'es'):
					language = 'sp'
				url = '%s&mainSearchCriteria.v.c=%s&informationRecipient.languageCode.c=%s' % (AppConfig.medlinePlusHealthDiagnosisICD9URL, query, language)
				rpcDiagnosis = urlfetch.create_rpc()
				urlfetch.make_fetch_call(rpcDiagnosis, url)
			except Exception,exD:
				logging.error('Errors downloading health diagnosis content: %s' % exD)
		
		#get hospital data
		if (userLat and userLon):
			hospitalData = self.getHospitalData(userLat, userLon,format)
			if (hospitalData):
				returnData += Formatter.dataComplex(format, 'hospital-records', hospitalData)
		
		if (rpcClinicalTrials):
			clinicalTrialsData = ''
			try:
			    resultClinicalTrials = rpcClinicalTrials.get_result()
			    if (resultClinicalTrials and resultClinicalTrials.status_code == 200):
					if (resultClinicalTrials.content):
						clinicalTrialsData = self.getClinicalTrialsData(minidom.parseString(resultClinicalTrials.content), format)
					else:
						logging.error('unable to retrieve clinical trials content')
						clinicalTrialsData = Formatter.data(format, 'error', 'Unable to retrieve content from provider')
			except Exception,ex:
				logging.error('Errors getting clinical trials content: %s' % ex)
				clinicalTrialsData = Formatter.data(format, 'error', 'Error(s) retrieving content from provider: %s' % ex)
		
			#append to the overall dataset
			returnData += Formatter.dataComplex(format, 'clinicaltrials-records', clinicalTrialsData)
		
		#fetch ICD-9 diagnosis data
		if (rpcDiagnosis):
			diagnosisData = ''
			try:
			    resultDiagnosis = rpcDiagnosis.get_result()
			    if (resultDiagnosis and resultDiagnosis.status_code == 200):
					if (resultDiagnosis.content):
						diagnosisData = self.getDiagnosisICD9Data(minidom.parseString(resultDiagnosis.content), format)
					else:
						logging.error('unable to retrieve diagnosis content')
						diagnosisData = Formatter.data(format, 'error', 'Unable to retrieve content from provider')
			except Exception,ex:
				logging.error('Errors getting diagnosis content: %s' % ex)
				diagnosisData = Formatter.data(format, 'error', 'Error(s) retrieving content from provider: %s' % ex)
			
			#append to the overall dataset
			returnData += Formatter.dataComplex(format, 'diagnosis-records', diagnosisData)
				
		#fetch health topic data
		if (rpcTopic):
			topicData = ''
			try:
			    resultTopic = rpcTopic.get_result()
			    if (resultTopic and resultTopic.status_code == 200):
					if (resultTopic.content):
						topicData = self.getTopicData(minidom.parseString(resultTopic.content), format,lan)
					else:
						logging.error('unable to retrieve health topic content')
						topicData = Formatter.data(format, 'error', 'Unable to retrieve content from provider')
			except Exception,ex:
				logging.error('Errors retrieving health topic content: %s' % ex)
				topicData = Formatter.data(format, 'error', 'Error(s) retrieving content from provider: %s' % ex)
		
			#append to the overall dataset
			returnData += Formatter.dataComplex(format, 'healthtopic-records', topicData)
			
		#output to the browser
		self.response.out.write(Formatter.dataWrapper(format, returnData))