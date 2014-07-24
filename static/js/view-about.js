//display about.html page
healthguide.views.About = new Ext.Panel({
	layout: Ext.is.Phone ? 'fit' : 'card',
	styleHtmlContent: true,
	
});


Ext.Ajax.request({
    url: '/static/html/about.html',
    success: function(rs){
        healthguide.views.About.update(rs.responseText);
    },
    scope: this
});