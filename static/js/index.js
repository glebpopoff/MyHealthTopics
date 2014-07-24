Ext.ns('healthguide', 'healthguide.views');

Ext.setup({
	name: "MyHealthGuide",
	icon: '/static/images/icon.png',
	glossOnIcon: false,
	tabletStartupScreen: '/static/images/tablet_startup.png',
    onReady: function() {
        healthguide.App = new healthguide.App({
            title: "MyHealthGuide"
        });
    }
});