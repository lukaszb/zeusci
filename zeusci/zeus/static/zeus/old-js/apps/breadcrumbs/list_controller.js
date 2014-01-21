zeus.module("BreadcrumbsApp.List", function (List, app, Backbone, Marionette, $, _) {

    List.Controller = {
        listBreadcrumbs: function () {
            var breadcrumbs = app.request("breadcrumbs");
            var view = new List.BreadcrumbsView({collection: breadcrumbs});
            app.breadcrumbsRegion.show(view);
        }
    }

});
