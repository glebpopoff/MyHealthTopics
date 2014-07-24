healthguide.views.SearchFilter = Ext.extend(Ext.form.FormPanel, {
    ui: 'green',
    cls: 'x-toolbar-dark',
    baseCls: 'x-toolbar',
    
    initComponent: function() {
        this.addEvents(
            /**
             * @event filter
             * Fires whenever the user changes any of the form fields
             * @param {Object} values The current value of each field
             * @param {Ext.form.FormPanel} form The form instance
             */
            'filter'
        );
        
        this.enableBubble('filter');
        
        Ext.apply(this, {
            defaults: {
                listeners: {
                    change: this.onFieldChange,
                    scope: this
                }
            },
            
            layout: {
                type: 'hbox',
                align: 'center'
            },
            
            items: [
                {
                    xtype: 'selectfield',
                    name: 'gender',
                    prependText: 'Gender:',
                    options: [
                        {text: 'Both',   value: ''},
                        {text: 'Male',   value: 'male'},
                        {text: 'Female', value: 'female'}
                    ]
                },
                {
                    xtype: 'spacer'
                },
                {
                    xtype: 'searchfield',
                    name: 'q',
                    placeholder: 'Search',
                    listeners : {
                        change: this.onFieldChange,
                        keyup: function(field, e) {
                            var key = e.browserEvent.keyCode;
                            
                            // blur field when user presses enter/search which will trigger a change if necessary.
                            if (key === 13) {
                                field.blur();
                            }
                        },
                        scope : this
                    }
                }
            ]
        });
            
        healthguide.views.SearchFilter.superclass.initComponent.apply(this, arguments);
    },
    
    /**
     * This is called whenever any of the fields in the form are changed. It simply collects all of the 
     * values of the fields and fires the custom 'filter' event.
     */
    onFieldChange : function(comp, value) {
        this.fireEvent('filter', this.getValues(), this);
    }
});

Ext.reg('search-filter', healthguide.views.SearchFilter);