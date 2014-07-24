var gpsCoords = 
	{
		lat: '',
		lon: ''
	};

var healthCenterFormFields = 
	{
		keywordField: new Ext.form.Text(
		{
			type: 'textfield',
			placeHolder: '',
			name : 'keyword',
			label: 'Keyword',
			useClearIcon: true,
			autoCapitalize : false
	   	}),
		zipField: new Ext.form.Text(
		{
			xtype: 'textfield',
			name : 'zip',
			label: 'Zip Code',
			placeHolder: '',
			useClearIcon: true,
			autoCapitalize : false
	   }),
	   searchTypeField: new Ext.form.Select(
		{
			xtype: 'selectfield',
			name: 'search_type',
			label: 'Search Type',
			options: [{
						text: 'Hospitals',
						value: 'hospitals'
					   }, 
					   {
						 text: 'Dialysis Centers',
						 value: 'dialysis'
						}
					  ]
		}),
	};

Ext.regModel('SearchResultsModel', {
	fields: [
		"id",
		"keyword",
		"condition",
		"zipcode", 
		"description",
		"image"
		]
});

//used for both hospital & dialysis center search
Ext.regModel('HospitalModel', {
	fields: [
		"hospital_id",
		"name",
        "address",
        "city",
        "state",
        "zip_code",
        "county",
        "phone",
        "hospital_type",
        "hospital_owner",
		"owner",
        "emergency_service",
        "geo_location",
        "distance",
		"in_center_hemo",
		"in_center_pd"
	]
	
});

var hospitalResultsStore = new Ext.data.Store({
	    model: 'HospitalModel',
	    autoLoad: false,
	    proxy: {
	        type: 'ajax',
	        method: 'get',
	        url : null,
	        extraParams: {},
	        reader: {
	            type: 'json',
	            root: ''
	        }
	    }
	});
/*
Ext.regModel('DialysisCenterModel' {
	fields: [
		"location_id",
		"name",
        "address",
        "address2",
        "city",
        "state",
        "zip_code",
        "owner",
        "phone",
        "in_center_hemo",
        "in_center_pd",
        "geo_location",
        "distance"
	]
	
});
*/			
var searchResultsStoreStatic = new Ext.data.Store({
    model: 'SearchResultsModel',
    autoLoad: true,
    data: [
	        {
				id: 'Asthma', 
				keyword: 'asthma',
				condition: 'Asthma',
				zipcode: '06032',
				description: 'Asthma is a chronic disease that affects your airways. Your airways are tubes that carry air in and out of your lungs. If you have asthma, the inside walls of your airways become sore and swollen. ', 
				image: 'http://www.nlm.nih.gov/medlineplus/images/asthma.jpg'
			},
			{
				id: 'Back Pain', 
				keyword: 'Back Pain',
				condition: 'Back Pain',
				zipcode: '06032',
				description: 'If you\'ve ever groaned, "Oh, my aching back!", you are not alone. Back pain is one of the most common medical problems, affecting 8 out of 10 people at some point during their lives. Back pain can range from a dull, constant ache to a sudden, sharp pain. Acute back pain comes on suddenly and usually lasts from a few days to a few weeks. Back pain is called chronic if it lasts for more than three months.', 
				image: 'http://www.nlm.nih.gov/medlineplus/images/lumbarvertebrae.jpg'
			},
			{
				id: 'Calcium', 
				keyword: 'Calcium',
				condition: 'Calcium',
				zipcode: '06032',
				description: 'You have more calcium in your body than any other mineral. Calcium has many important jobs. The body stores more than 99 percent of its calcium in the bones and teeth to help make and keep them strong. The rest is throughout the body in blood, muscle and the fluid between cells. Your body needs calcium to help muscles and blood vessels contract and expand, to secrete hormones and enzymes and to send messages through the nervous system.', 
				image: 'http://www.nlm.nih.gov/medlineplus/images/calcium.jpg'
			}
	        
	    ]
});

//app navigation
healthguide.Structure = [
    {
        text: 'Health Library',
        card: "healthguide.views.Themes",
        leaf: true
    },
    
    {
        text: 'Health Center Finder',
        card: "healthguide.views.HealthCenterForm",
        leaf: true
    },

	{
        text: 'Bookmarks',
        card: "healthguide.views.Bookmarks",
        leaf: true
    },

	{
        text: 'About',
        card: "healthguide.views.About",
        leaf: true
    },
];

Ext.regModel('HealthGuideNav', {
    fields: [
        {name: 'text',        type: 'string'},
        {name: 'preventHide', type: 'boolean'},
        {name: 'cardSwitchAnimation'},
        {name: 'card',        type: 'string'}
    ]
});

healthguide.StructureStore = new Ext.data.TreeStore({
    model: 'HealthGuideNav',
    root: {
        items: healthguide.Structure
    },
    proxy: {
        type: 'ajax',
        reader: {
            type: 'tree',
            root: 'items'
        }
    }
});

