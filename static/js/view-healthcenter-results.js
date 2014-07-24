healthguide.views.HealthCenterResults = new Ext.Panel({
        layout: Ext.is.Phone ? 'fit' : 'card',  
  		dockedItems: [{
		            xtype: 'toolbar',
		            title: 'Results',
		            items: [{
		                ui: 'back',
		                text: 'Back',
		                scope: this,
		                handler: function(){
		                    healthguide.App.setActiveItem(this.prevCard, 'slide');
		                }
		            }]
				}],
        items: [
            {
                //width: Ext.is.Phone ? undefined : 300,
                height: 500,
                xtype: 'list',
                store: hospitalResultsStore,
                itemTpl: '<div class="healthcenter-list-data"><div class="healthcenter-list-data-info"><h3>{name}</h3>{address}<br/>{city}, {state} {zip_code}<br/>Phone: {phone}</div><div class="healthcenter_miles_info">{distance}</div><tpl if="in_center_hemo">HEMO</tpl><tpl if="in_center_pd">PD</tpl></div>',
                onItemTap: function(item, index) {
                    var me = this,
                        recordData = this.store.getAt(index).data;
						console.log('Selected: ' + recordData.name)
                    
                }
            }
        ]
    });