zeus.module("Entities", (Entities, app, Backbone, Marionette, $, _, zeus_project) ->
    Entities.Project = Backbone.Model.extend({
    })

    getProject = () ->
        return zeus_project

    app.reqres.setHandler "project:current", () ->
        return getProject()
, zeus_project)
