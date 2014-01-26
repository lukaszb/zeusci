zeus.simpleModule('apps.projects.views', function (views, Marionette) {

    views.ProjectDetails = zeus.views.View.extend({
        template: "#project-details-template",
        modelContextName: "project",

        events: {
            "click .show-buildset": "showBuildset"
        },

        serializeData: function () {
            var data = zeus.views.View.prototype.serializeData.call(this);
            data.project = zeus.request('project').toJSON();
            return data;
        },

        showBuildset: function (event) {
            event.preventDefault();
            event.stopPropagation();
            var number = this.getBuildsetNumber(event);
            zeus.trigger('show:buildset', this.model.get('name'), number)
        },

        getBuildsetNumber: function (event) {
            var el = $(event.target);
            return el.attr('buildsetNumber');
        }
    });


    views.BuildsetDetails = zeus.views.View.extend({
        template: "#buildset-details-template",
        modelContextName: "buildset"
    });

}, Marionette);
