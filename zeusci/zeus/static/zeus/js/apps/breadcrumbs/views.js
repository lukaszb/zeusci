zeus.simpleModule('apps.breadcrumbs.views', function (views) {
    views.BreadcrumbsView = zeus.views.View.extend({
        template: '#breadcrumbs-template',
        collectionContextName: 'breadcrumbs'
    });
});
