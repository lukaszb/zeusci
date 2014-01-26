zeus.simpleModule('apps.projects.models', function (models, Backbone) {

    // Project
    models.Project = Backbone.Model.extend({});

    zeus.reqres.setHandler("project", function () {
        return new models.Project(zeus.project);
    });


    // Buildset
    models.Buildset = Backbone.Model.extend({
        url: function () {
            return zeus.project.uri + '/buildsets/' + this.get('number');
        }
    });

    zeus.reqres.setHandler("buildset:current", function () {
        return models.buildset;
    });

    zeus.reqres.setHandler("buildset", function (buildsetNumber) {
        return new models.Buildset({number: buildsetNumber});
    });

}, Backbone);
