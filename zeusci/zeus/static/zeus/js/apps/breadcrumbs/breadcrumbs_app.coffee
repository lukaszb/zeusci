@zeus.module "BreadcrumbsApp", (BreadcrumbsApp, app, Backbone, Marionette, $, _) ->


    console.log " -> BreadcrumbsApp"

    show = ->
        #controller = new BreadcrumbsApp.List.Controller
            #region: app.breadcrumbsRegion
        #view = controller.getListView()
        #region.show view
        BreadcrumbsApp.List.Controller.listBreadcrumbs()
        console.log "showed"


    app.on "start", ->
        # initiate breadcrumbs
        console.log "requesting breadcrumbs"
        app.request("breadcrumbs")
        show()
