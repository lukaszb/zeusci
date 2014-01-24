zeus.simpleModule('apps.breadcrumbs', function (breadcrumbsApp, region) {

    var showBreadcrumbs = function () {
        var breadcrumbs = zeus.request('breadcrumbs');
        var view = new breadcrumbsApp.views.BreadcrumbsView({
            collection: breadcrumbs
        });
        region.show(view);
    };

    zeus.on('start', showBreadcrumbs);
}, zeus.breadcrumbsRegion);
