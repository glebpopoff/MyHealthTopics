My Health Topics
===============

The source code for the Health2 initiative that took second place in 2012 competition: http://acsyshealthguide.appspot.com/ 

The application combines a number of health data feeds, such as health topics, hospitals, clinical trials, health news, and FDA health updates. There's also integration with Google Translate API to provide translation support for Spanish.

The app was built using an early versin of the JQuery mobile framework and has 

There's also an API for all the data sources: http://acsyshealthguide.appspot.com/api

Last but not least, we did some work with the AppEngine Data Bulk Upload api - take a look at the DataLoaderDialysis.py and load_data_dialysis.sh to get an example how we uploaded large datasets (dialysis data) into the AppEngine. We also did some work with the AppEngine geofencing API (geobox values, proximity search): DataLoaderHospitalInfo.py

Have fun!

![alt tag](https://raw.githubusercontent.com/glebpopov/MyHealthTopics/master/static/images/screenshot1.png)

![alt tag](https://raw.githubusercontent.com/glebpopov/MyHealthTopics/master/static/images/screenshot2.png)

![alt tag](https://raw.githubusercontent.com/glebpopov/MyHealthTopics/master/static/images/screenshot3.png)
