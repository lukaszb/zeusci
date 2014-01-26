zeus.simpleModule('apps.breadcrumbs.models', function (models, Backbone) {

    var getBreadcrumbs = function () {
        var breadcrumbs = [{name: "Projects", url: "/"}];

        var project = zeus.request("project");
        if (project) {
            breadcrumbs.push({
                name: project.get('name'),
                url: project.get('url')
            });
        }

        var buildset = zeus.request('buildset:current');
        if (buildset) {
            breadcrumbs.push({
                name: 'Buildset ' + buildset.get('number'),
                url: buildset.get('url')
            });
        }
        return breadcrumbs;
    }


    models.Breadcrumb = Backbone.Model.extend({});
    models.BreadcrumbList = Backbone.Collection.extend({
        model: models.Breadcrumb,

        refresh: function () {
            this.reset(getBreadcrumbs());
        }
    });

    models.breadcrumbs = new models.BreadcrumbList();

    zeus.on('breadcrumbs:refresh', function () {
        models.breadcrumbs.refresh();
    });

    zeus.reqres.setHandler("breadcrumbs", function () {
        if (models.breadcrumbs === undefined) {
            models.breadcrumbs = new models.BreadcrumbList();
        }
        models.breadcrumbs.refresh();
        return models.breadcrumbs;
    });

}, Backbone);
