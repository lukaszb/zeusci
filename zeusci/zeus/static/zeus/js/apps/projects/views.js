zeus.simpleModule('apps.projects.views', function (views, Marionette, $) {

    views.ProjectLayout = Marionette.Layout.extend({
        template: "#project-layout-template",

        regions: {
            contentRegion: "#project-content-region"
        }
    });


    views.ProjectDetails = zeus.views.View.extend({
        template: "#project-details-template",
        modelContextName: "project",

        events: {
            "click .show-buildset": "showBuildset"
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

}, Marionette, $);
