zeus.module "Entities", (Entities, app, Backbone, Marionette, $, _) ->


    class Entities.Breadcrumb extends Backbone.Model


    class Entities.Breadcrumbs extends Backbone.Collection
        model: Entities.Breadcrumb


    getBreadcrumbs = ->
        breadcrumbs = [{name: "Projects", url: "/"}]

        project = app.request "project:current"
        if project
            breadcrumbs.push({name: project.name, url: project.url})

        Entities.breadcrumbs = new Entities.Breadcrumbs(breadcrumbs)
        return Entities.breadcrumbs


    app.reqres.setHandler "breadcrumbs", getBreadcrumbs
