@zeus.module "BreadcrumbsApp.List", (List, app, Backbone, Marionette, $, _) ->


    List.Controller = {
        listBreadcrumbs: ->
            breadcrumbs = app.request "breadcrumbs"
            view = new List.BreadcrumbsView({collection: breadcrumbs})
            app.breadcrumbsRegion.show(view)
    }
