zeus.simpleModule('apps.breadcrumbs.views', function (views, $) {
    views.BreadcrumbsView = zeus.views.View.extend({
        template: '#breadcrumbs-template',
        collectionContextName: 'breadcrumbs',

        events: {
            'click .breadcrumb-item': 'onBreadcrumbClick'
        },

        onBreadcrumbClick: function (event) {
            event.preventDefault();
            zeus.navigate($(event.target).attr('href'), {trigger: true});
        }
    });
}, $);
