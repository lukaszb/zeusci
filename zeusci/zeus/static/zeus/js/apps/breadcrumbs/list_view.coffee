@zeus.module "BreadcrumbsApp.List", (List, App, Backbone, Marionette, $, _) ->


    class List.BreadcrumbsView extends App.Views.ItemView
        template: "#breadcrumbs-template"
        contextCollectionName: 'breadcrumbs'
