zeus.simpleModule('apps.breadcrumbs.models', function (models, Backbone) {

    models.Breadcrumb = Backbone.Model.extend({});
    models.BreadcrumbList = Backbone.Collection.extend({
        model: models.Breadcrumb
    });


    var getBreadcrumbs = function () {
        var breadcrumbs = [{name: "Projects", url: "/"}];

        var project = zeus.request("project");
        if (project) {
            breadcrumbs.push({
                name: project.get('name'),
                url: project.get('url')
            });
        }

        models.breadcrumbs = new models.BreadcrumbList(breadcrumbs);
        return models.breadcrumbs;
    }

    zeus.reqres.setHandler("breadcrumbs", getBreadcrumbs);

}, Backbone);
