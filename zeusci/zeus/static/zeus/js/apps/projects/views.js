zeus.simpleModule('apps.projects.views', function (views, Marionette) {

    views.ProjectDetails = zeus.views.View.extend({
        template: "#project-details-template",

        serializeData: function () {
            var data = Marionette.Layout.prototype.serializeData.call(this);
            data.project = zeus.request('project').toJSON();
            return data;
        }
    });

}, Marionette);
