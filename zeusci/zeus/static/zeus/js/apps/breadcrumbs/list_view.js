zeus.module("BreadcrumbsApp.List", function (List, App, Backbone, Marionette, $, _) {


    List.BreadcrumbsView = App.Views.ItemView.extend({
        template: "#breadcrumbs-template",
        contextCollectionName: 'breadcrumbs',
    });

});
