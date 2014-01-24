zeus.simpleModule('apps.projects.models', function (models, Backbone) {

    models.Project = Backbone.Model.extend({});

    var getProject = function () {
        return new models.Project(zeus.project);
    }

    app.reqres.setHandler("project", getProject);

}, Backbone);
