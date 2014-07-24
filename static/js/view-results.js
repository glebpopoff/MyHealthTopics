healthguide.views.Themes = new Ext.Panel({
        layout: Ext.is.Phone ? 'fit' : 'card',    
        items: [
            {
                //width: Ext.is.Phone ? undefined : 300,
                height: 500,
                xtype: 'list',
                store: searchResultsStoreStatic,
                itemTpl: '<div class="theme_choice">{keyword}</div>',
                onItemTap: function(item, index) {
                    var me = this,
                        recordData = this.store.getAt(index).data;

                    if (!themeSheets[recordData.id]) {
                        this.setLoading(true);
                        appendStyleSheet("../../resources/css/" + recordData.file, function(sheet) {
                            themeSheets[recordData.id] = sheet;
                            setActiveSheet(sheet);
                            me.setLoading(false);
                        });
                    }
                    else {
                        setActiveSheet(themeSheets[recordData.id]);
                    }
                }
            }
        ]
    });


healthguide.views.Results = Ext.extend(Ext.Panel, {
    layout: 'card',
	fullscreen: true,
    initComponent: function() {

        this.settingsIcon = new Ext.Button({
		            text: 'Add',
		            handler: this.onSettingsTap,
					scope: this
		        });

        this.list = new Ext.List({
            cls: 'timeline',
			emptyText   : '<p class="no-searches">Unable to retrieve data</p>',
			store: searchResultsStoreStatic,
            itemCls: 'weatheritem',
			itemTpl: new Ext.XTemplate(
				'<span class="name">{location}</span>'
            )
        });

		this.list.on('selectionchange', this.onSelect, this);
		
		this.list.on('render', function(){
		            //this.list.store.load();
		            this.list.el.mask('<span class="top"></span><span class="right"></span><span class="bottom"></span><span class="left"></span>', 'x-spinner', false);
		        }, this);

		this.listpanel = new Ext.Panel({
            layout: 'fit',
            items: this.list,
            dockedItems: [{
                xtype: 'search-filter',
                dock: 'top'
            }
			],
            listeners: {
                activate: { fn: function(){
                    this.list.getSelectionModel().deselectAll();
					Ext.repaint();
                }, scope: this }
                
            }
        });
        
        this.items = this.listpanel;
       	healthguide.views.Results.superclass.initComponent.call(this);
    },

	onSettingsTap: function() {
	        var addLocationCard = new todaysweather.views.AddNewLocation({
                prevCard: this.listpanel
            });
			this.setActiveItem(addLocationCard, 'slide');
	        
	    },
    
    onSelect: function(selectionmodel, records){
		if (records[0] !== undefined) {
            todayWeatherForecastToolbar.getDockedItems()[0].setTitle(records[0].raw.location);
			fiveDayWeatherForecastToolbar.getDockedItems()[0].setTitle(records[0].raw.location);

			weatherForecastStore.proxy.url = '/weather?loc=' + records[0].raw.lookup_id;
			weatherForecastStore.load();
	
			//show first screen
			todaysweather.App.setActiveItem(0, 'flip');
		
			todaysweather.App.doLayout();
        }
    }
});

Ext.reg('results-screen', healthguide.views.Results);