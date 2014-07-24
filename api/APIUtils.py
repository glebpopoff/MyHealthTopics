from UserString import MutableString
import re
import logging
import Formatter
from xml.dom import minidom
from xml.sax.saxutils import escape
import urllib
from api import CharReplacementMap
import AppConfig

#get health news
def getHealthNews(lan='en',format='json'):
	returnData = MutableString()
	returnData = ''
	if (lan == 'es'):
		dom = minidom.parse(urllib.urlopen(AppConfig.medlinePlusHealthNewsSpanishURL))
	else:
		dom = minidom.parse(urllib.urlopen(AppConfig.medlinePlusHealthNewsEnglishURL))
	rssTitle = MutableString()
	rssDescription = MutableString()
	rssURL = MutableString()
	for node in dom.getElementsByTagName('item'):
		for item_node in node.childNodes:
			rssTitle = ''
			rssDescription = ''
			rssURL = ''
			#item title
			if (item_node.nodeName == "title"):
				for text_node in item_node.childNodes:
					if (text_node.nodeType == node.TEXT_NODE):
						rssTitle += text_node.nodeValue
			#description
			if (item_node.nodeName == "description"):
				for text_node in item_node.childNodes:
					rssDescription += text_node.nodeValue
			#link to URL
			if (item_node.nodeName == "link"):
				for text_node in item_node.childNodes:
					rssURL += text_node.nodeValue
			
			if (format == 'json'):
				startTag = '{'
				endTag = '},'
				
				#cleanup
				#rssTitle = re.sub("\"", "'", rssTitle)
				rssTitle = re.sub("\n", "", rssTitle)
				rssTitle = re.sub("\"", "\\\"", rssTitle)
				rssDescription = re.sub("\"", "\\\"", rssDescription)
				rssDescription = re.sub("\n", "", rssDescription)
				rssDescription = re.sub("\t", " ", rssDescription)
				rssDescription = re.sub("\r", "", rssDescription)
				
				if (len(rssDescription) > 0):
					rssDescription = Formatter.data(format, 'description', escape(rssDescription))[:-1]
			else:
				startTag = '<record>'
				endTag = '</record>'		
				if (len(rssDescription) > 0):
					rssDescription = Formatter.data(format, 'description', escape(rssDescription))								
			
			if (len(rssTitle) > 0):
				returnData += startTag + Formatter.data(format, 'title', rssTitle)
				
			if (len(rssURL) > 0):
				returnData += Formatter.data(format, 'url', rssURL) 
			
			if (len(rssDescription) > 0 ):
				returnData += rssDescription + endTag
	
	return returnData
				
#parse health topic data
def parseHealthTopicContent(format,node):
	if (node):
		contentTitle = MutableString()
		contentAltTitle = MutableString()
		contentSummary = MutableString()
		contentTitle = ''
		contentAltTitle = ''
		contentSummary = ''
		
		for content_node in node.childNodes:
			#get title
			if (content_node and content_node.nodeName == 'content' and content_node.attributes['name'].value == "title"):
				for text_node in content_node.childNodes:
					contentTitle += CharReplacementMap.remove_html_tags(text_node.nodeValue)
			#get alt title
			"""if (content_node and content_node.nodeName == 'content' and content_node.attributes['name'].value == "altTitle"):
				for text_node in content_node.childNodes:
					contentAltTitle += remove_html_tags(text_node.nodeValue)
			"""
			#get content	
			if (content_node and content_node.nodeName == 'content' and content_node.attributes['name'].value == "FullSummary"):
				for text_node in content_node.childNodes:
					contentSummary += text_node.nodeValue
		
		#replace HTML tags with friendly tags (that will be replaced back to HTML later)
		#contentSummary = CharReplacementMap.translate_tags_from_html(contentSummary)
		#now strip HTML garbage
		#contentSummary = CharReplacementMap.remove_html_tags(contentSummary)
		
		returnData = MutableString()
		returnData = ''			
		if (format == 'json'):
			startTag = '{'
			endTag = '},'
			
			#cleanup
			contentTitle = re.sub("\n", "", contentTitle)
			contentTitle = re.sub("\"", "\\\"", contentTitle)
			contentAltTitle = re.sub("\n", "", contentAltTitle)
			contentAltTitle = re.sub("\r", "", contentAltTitle)
			contentAltTitle = re.sub("\"", "\\\"", contentAltTitle)
			contentSummary = re.sub("\"", "\\\"", contentSummary)
			contentSummary = re.sub("\n", "", contentSummary)
			contentSummary = re.sub("\t", " ", contentSummary)
			contentSummary = re.sub("\r", "", contentSummary)
			
			if (len(contentSummary) > 0):
				contentSummary = Formatter.data(format, 'summary', escape(contentSummary))[:-1]
		else:
			startTag = '<record>'
			endTag = '</record>'		
			if (len(contentSummary) > 0):
				contentSummary = Formatter.data(format, 'summary', escape(contentSummary))
		
		if (len(contentTitle) > 0):
			returnData += startTag + Formatter.data(format, 'title', escape(contentTitle))

		if (len(contentAltTitle) > 0):
			returnData += Formatter.data(format, 'alt_title', escape(contentAltTitle)) 

		if (len(contentSummary) > 0 ):
			returnData += contentSummary + endTag

		return returnData

#parse diagnosis ICD9 data
def parseHealthDiagnosisICD9Content(format,node):
	if (node):
		contentTitle = MutableString()
		contentLink = MutableString()
		contentSummary = MutableString()
		contentTitle = ''
		contentLink = ''
		contentSummary = ''
		
		for content_node in node.childNodes:
			#get title
			if (content_node and content_node.nodeName == 'title'):
				for text_node in content_node.childNodes:
					contentTitle += text_node.nodeValue
			#get link
			if (content_node and content_node.nodeName == 'link'):
				contentLink += content_node.attributes['href'].value
			#get content	
			if (content_node and content_node.nodeName == 'summary'):
				for text_node in content_node.childNodes:
					contentSummary += text_node.nodeValue
		
		#replace HTML tags with friendly tags (that will be replaced back toHTML later)
		#contentSummary = CharReplacementMap.translate_tags_from_html(contentSummary)
		#now strip HTML garbage
		#contentSummary = CharReplacementMap.remove_html_tags(contentSummary)
		
		returnData = MutableString()
		returnData = ''			
		if (format == 'json'):
			startTag = '{'
			endTag = '},'

			#cleanup
			contentTitle = re.sub("\n", "", contentTitle)
			contentTitle = re.sub("\"", "\\\"", contentTitle)
			contentLink = re.sub("\n", "", contentLink)
			contentLink = re.sub("\"", "\\\"", contentLink)
			contentSummary = re.sub("\"", "\\\"", contentSummary)
			contentSummary = re.sub("\n", "", contentSummary)
			contentSummary = re.sub("\r", "", contentSummary)
			contentSummary = re.sub("\t", " ", contentSummary)
			
			if (len(contentSummary) > 0):
				contentSummary = Formatter.data(format, 'summary', escape(contentSummary))[:-1]
		else:
			startTag = '<record>'
			endTag = '</record>'		
			if (len(contentSummary) > 0):
				contentSummary = Formatter.data(format, 'summary', escape(contentSummary))
		
		if (len(contentTitle) > 0):
			returnData += startTag + Formatter.data(format, 'title', escape(contentTitle))

		if (len(contentLink) > 0):
			returnData += Formatter.data(format, 'link', escape(contentLink)) 

		if (len(contentSummary) > 0 ):
			returnData += contentSummary + endTag

		return returnData
		
#parse clinical trials RSS
def parseClinicalTrialsContent(format,node):
	if (node):
		contentTitle = MutableString()
		contentLink = MutableString()
		contentSummary = MutableString()
		contentStatus = MutableString()
		contentTitle = ''
		contentLink = ''
		contentSummary = ''
		contentStatus = ''

		for content_node in node.childNodes:
			#get title
			if (content_node and content_node.nodeName == 'title'):
				for text_node in content_node.childNodes:
					contentTitle += text_node.nodeValue
			#get link
			if (content_node and content_node.nodeName == 'url'):
				for text_node in content_node.childNodes:
					contentLink += text_node.nodeValue
			#get status
			if (content_node and content_node.nodeName == 'status'):
				for text_node in content_node.childNodes:
					contentStatus += text_node.nodeValue
			#get content	
			if (content_node and content_node.nodeName == 'condition_summary'):
				for text_node in content_node.childNodes:
					contentSummary += text_node.nodeValue

		returnData = MutableString()
		returnData = ''			
		if (format == 'json'):
			startTag = '{'
			endTag = '},'

			#cleanup
			contentStatus = re.sub("\n", "", contentStatus)
			contentStatus = re.sub("\"", "\\\"", contentStatus)
			contentTitle = re.sub("\n", "", contentTitle)
			contentTitle = re.sub("\"", "\\\"", contentTitle)
			contentTitle = re.sub("\t", " ", contentTitle)
			contentLink = re.sub("\n", "", contentLink)
			contentLink = re.sub("\"", "\\\"", contentLink)
			contentSummary = re.sub("\"", "\\\"", contentSummary)
			contentSummary = re.sub("\n", "", contentSummary)
			contentSummary = re.sub("\t", " ", contentSummary)

			if (len(contentSummary) > 0):
				contentSummary = Formatter.data(format, 'summary', escape(contentSummary))[:-1]
		else:
			startTag = '<record>'
			endTag = '</record>'		
			if (len(contentSummary) > 0):
				contentSummary = Formatter.data(format, 'summary', escape(contentSummary))

		if (len(contentTitle) > 0):
			returnData += startTag + Formatter.data(format, 'title', escape(contentTitle))

		if (len(contentLink) > 0):
			returnData += Formatter.data(format, 'link', escape(contentLink)) 

		if (len(contentStatus) > 0):
			returnData += Formatter.data(format, 'status', escape(contentStatus))

		if (len(contentSummary) > 0 ):
			returnData += contentSummary + endTag

		return returnData