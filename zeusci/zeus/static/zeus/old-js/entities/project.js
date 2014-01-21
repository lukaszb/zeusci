zeus.module("Entities", function (Entities, app, Backbone, Marionette, $, _, zeus_project) {
    Entities.Project = Backbone.Model.extend({})

    var getProject = function () {
        return zeus_project;
    }

    app.reqres.setHandler("project:current", getProject);

}, zeus_project)
