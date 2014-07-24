healthguide.views.HealthCenterForm = new Ext.Panel({
    scroll: 'vertical',
	type: 'vbox',
	align: 'stretch',
    items: [
	{
        xtype: 'fieldset',
		instructions: 'This form allows you to search national hospital and dialysis database.',
		items: [
				healthCenterFormFields.keywordField,
				healthCenterFormFields.zipField,
				{
					xtype: 'checkboxfield',
                    name : 'use_mylocation',
                    label: 'Use GPS for My Location',
					listeners: {
								check: function()
								{
									console.log('Getting GPS Coordinates');
								
									var geoService = new Ext.util.GeoLocation({
								            autoUpdate: false
								        });
								geoService.on('beforelocationupdate', 
									function()
									{
								        Ext.getBody().mask('Loading...', 'x-mask-loading', false);
								    }
								, this);
								geoService.on('locationupdate', 
									function(coords) 
									{
										console.log('Lat=' + coords.latitude + ',Long=' + coords.longitude);
										gpsCoords.lat = coords.latitude;
										gpsCoords.lon = coords.longitude
										Ext.getBody().mask('Loading...', 'x-mask-loading', false);
										Ext.Ajax.request({
				                            url: '/geo?ll=' + coords.latitude + ',' + coords.longitude,
				                            success: function(response, opts) {
												var jsonObj = (response.responseText && response.responseText.indexOf('success') != -1) 
															? eval("(" + response.responseText + ")") : null;
												if (jsonObj && jsonObj.status == 'success')
												{
													formFields.zipField.setValue(jsonObj.zip);
												} else 
												{
													Ext.Msg.alert('Error', 'Unable to retrieve zipcode based on GPS', Ext.emptyFn);
								                }
											}
										});
										Ext.getBody().unmask();
									}
								, this);
								geoService.updateLocation();

							}
						}
				},
				healthCenterFormFields.searchTypeField,
				{
					type: 'vbox',
					defaults: {xtype: 'button', flex: 1, style: 'margin: .5em;'},
		            items: [
	            
						{ xtype: 'spacer'},
						{
				            text: ' Search ',
							width: '250px',
						 	ui: 'confirm',
				            handler: function() 
							{
								if (healthCenterFormFields.zipField.getValue())
								{
									console.log('Performing Search. Zip: ' + healthCenterFormFields.zipField.getValue() + '. Search Type: ' + healthCenterFormFields.searchTypeField.getValue());
								
									//hospital search
									if (healthCenterFormFields.searchTypeField.getValue() == 'hospitals')
									{
										//call ajax service
										hospitalResultsStore.proxy.url = '/api/hospital-search/zip/' + healthCenterFormFields.zipField.getValue() + '/format/json';
									} else
									{
										//dialysis center search
										hospitalResultsStore.proxy.url = '/api/dialysis-center-search/zip/' + healthCenterFormFields.zipField.getValue() + '/format/json';
									}
									hospitalResultsStore.load();

									//show results screen
									card = healthguide.views.HealthCenterResults;
									healthguide.App.setActiveItem(card, 'slide');
						            healthguide.App.currentCard = card;

									//todaysweather.App.doLayout();
								} else
								{
									Ext.Msg.alert('', 'Please Enter Zip Code', Ext.emptyFn);
								}
							},
							success: function(e) 
							{
				            }
			            }
					]
				}
			]
		}]
 });