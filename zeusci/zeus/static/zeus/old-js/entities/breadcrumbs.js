zeus.module("Entities", function (Entities, app, Backbone, Marionette, $, _) {

    Entities.Breadcrumb = Backbone.Model.extend({});

    Entities.Breadcrumbs = Backbone.Collection.extend({
        model: Entities.Breadcrumb
    });

    var getBreadcrumbs = function () {
        var breadcrumbs = [{name: "Projects", url: "/"}];

        var project = app.request("project:current");
        if (project) {
            breadcrumbs.push({name: project.name, url: project.url});
        }

        Entities.breadcrumbs = new Entities.Breadcrumbs(breadcrumbs);
        return Entities.breadcrumbs;
    }

    app.reqres.setHandler("breadcrumbs", getBreadcrumbs);
});
