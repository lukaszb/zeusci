@zeus = do (Backbone, Marionette) ->

    app = new Marionette.Application

    app.addRegions({
        mainRegion: "#main-region",
        breadcrumbsRegion: "#breadcrumbs-region",
    })

    return app

@app = @zeus  # TODO: just a temp shortcut
