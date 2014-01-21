zeus.module("BreadcrumbsApp", function (BreadcrumbsApp, app, Backbone, Marionette, $, _) {
    var show = function () {
        BreadcrumbsApp.List.Controller.listBreadcrumbs();
    }


    app.on("start", function () {
        // initiate breadcrumbs
        console.log("requesting breadcrumbs");
        app.request("breadcrumbs");
        show();
    });
});
