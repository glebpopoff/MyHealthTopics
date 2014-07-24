#lambda expression (short inline function)
bulkloader.Loader.__init__(self, 'Album',
                                   [('title', str),
                                    ('artist', str),
                                    ('publication_date',
                                     lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
                                    ('length_in_minutes', int)
                                   ])

#delete all entities
db.delete(HospitalGeoBox.all()) 


#read CSV file
fileAddress = open(os.path.join(os.path.dirname(__file__), AppConfig.hospitalComparisonAddressFile), 'rU') 
fileReaderAddress = csv.reader(fileAddress)
lineNum = 0
for addressRow in fileReaderAddress:
	if (lineNum > 0):
		try:
			hospID = addressRow[0]
			hospName = addressRow[1]
			hospAddress1 = addressRow[2]
			hospCity = addressRow[5]
			hospState = addressRow[6]
			hospZip = addressRow[7]
			hospCounty = addressRow[8]
			hospPhone = addressRow[9]
			hospType = addressRow[10]
			hospOwner = addressRow[11]
			hospEmergency = addressRow[12]
			hospLat = addressRow[14]
			hospLon = addressRow[15]
			
			if (hospID and hospName and hospAddress1 and hospCity and 
			    hospState and hospZip and hospPhone and hospLat and hospLon and hospLat != '0' and hospLon != '0'):
				#create new entity
				hospID.replace("'", "")
				gb = geobox2.Geobox(float(hospLat), float(hospLon))
				dbKey = 'key_%s' % (hospID)
				print 'saveLocation: creating new instance. Using key=%s' % dbKey
				locRec = HospitalInfo(key_name=dbKey)
				locRec.hospital_id = hospID
				locRec.name = hospName
				locRec.address = hospAddress1
				locRec.city = hospCity
				locRec.state = hospState
				locRec.location = db.GeoPt(float(hospLat), float(hospLon))
				locRec.zip_code = hospZip
				locRec.county = hospCounty
				locRec.phone = hospPhone
				locRec.hospital_type = hospType
				locRec.hospital_owner = hospOwner
				locRec.emergency_service = hospEmergency
				locRec.geoboxes = gb.storage_geoboxes()
				logging.debug('save: about to save')
				locRec.put()
			
		except Exception, exp:
			print 'DataLoaderHandler Exception: %s' % str(exp)