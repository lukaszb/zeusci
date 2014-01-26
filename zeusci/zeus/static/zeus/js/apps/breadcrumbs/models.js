zeus.simpleModule('apps.breadcrumbs.models', function (models, Backbone) {

    var getBreadcrumbs = function () {
        var breadcrumbs = [{name: "Projects", url: "/"}];

        var project = zeus.request("project");
        if (project) {
            var projectUrl = project.get('url').replace(/\/$/, '');

            breadcrumbs.push({
                name: project.get('name'),
                url: projectUrl
            });
            var url = zeus.getCurrentRoute();
            var match = url.match(/buildsets\/(\d+)/);
            if (match) {
                var buildsetNumber = match[1];
                breadcrumbs.push({
                    name: "Buildset " + buildsetNumber,
                    url: projectUrl + '/buildsets/' + buildsetNumber
                });
            }
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
