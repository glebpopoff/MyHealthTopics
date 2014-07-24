#
# Health 2.0 Challenge App by JakeB & GlebP
# Acsys Interactive, 2011

# GeoConverter: converts hospital address into GPS coordinates and saves that
# The resulting data file will contain hospital id, lat, lon 
#

import urllib
import urllib2
import csv
import sys
import os

file = open(os.path.join(os.path.dirname(__file__), 'data/dialysis_locations.csv'), 'rU') 
fileReader = csv.reader(file)
outputFile = open('/Users/glebp/Projects/AppEngine/acsyshealthguide/api/data/dialysis_locations-geo-coordinates.csv', 'w')
geoLocationDictionary = {}
for row in fileReader:
	print 'Processing: ID=%s' % (row[0])
	#lookup based on address1, city, state, zip
	if (row[2] != '' and row[4] != '' and row[5] != '' and row[6] != ''):
		#reverse geolookup
		locationGeoLat = ''
		locationGeoLon = ''
		try:
			physAddr = row[2] + "," + row[4] + "," + row[5] + " " + row[6]
			#poor man's URL encoding
			urlEncodedAddr = physAddr.replace(' ', '+')
			#lets see if we have this in the dictionary
			if geoLocationDictionary.has_key(urlEncodedAddr):
				print 'Using Saved Coordinates'
				geoKey = geoLocationDictionary[urlEncodedAddr]
				tmpArr = geoKey.split(',')
				locationGeoLat = tmpArr[0]
				locationGeoLon = tmpArr[1]
			else:
				#get coordinates from google maps
				geoURL = "%s%s&%s" % ("http://maps.google.com/maps/geo?q=",urlEncodedAddr,"output=csv")
				print 'Getting Geo Coordinates: %s' % geoURL
				response = urllib2.urlopen(geoURL)
				geoData = response.read()
				#should get this: 200,8,40.7370090,-73.9908550
				if geoData:
					print 'Got Response'
					tmpArr = geoData.split(',')
					locationGeoLat = tmpArr[2]
					locationGeoLon = tmpArr[3]
					#put in a dictionary so we can reuse later
					geoLocationDictionary[urlEncodedAddr] = "%s,%s" % (locationGeoLat, locationGeoLon)
				else:
					locationGeoLat = ''
					locationGeoLon = ''
		except:
			e = sys.exc_info()[1]
			print 'Cannot get geo coordinates', e
			locationGeoLat = ''
			locationGeoLon = ''
	else:
		print 'Invalid Address'
	
	if (locationGeoLat != '' and locationGeoLon != ''):
		print 'Writing to file'
		outputFile.write(row[0])
		outputFile.write(',')
		outputFile.write('%s,%s' % (locationGeoLat,locationGeoLon))
		outputFile.write('\n')
	print '-------------------'
outputFile.close()