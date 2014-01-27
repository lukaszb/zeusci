zeus.simpleModule('apps.projects', function (projects, region, _, Marionette) {

    projects.Controller = Marionette.Controller.extend({
        projectLayoutView: null,
        contentRegion: null,

        initialize: function (options) {
            this.project = options.project;
            this.region = options.region;
            _.bindAll(this,
                'initializeLayout',
                'showProject',
                'showProjectDetails',
                'showBuildset'
            );
            this.initializeLayout();
        },

        initializeLayout: function () {
            this.layout = new projects.views.ProjectLayout({
                model: this.project
            });
            this.contentRegion = this.layout.contentRegion;
            this.region.show(this.layout);
        },

        showProject: function () {
            console.log(" => show project");
            this.showProjectDetails();
            zeus.navigate(zeus.project.url);
        },

        showProjectDetails: function () {
            var view = new projects.views.ProjectDetails({model: this.project});
            this.contentRegion.show(view);
        },

        showBuildset: function (name, number) {
            console.log(" => show buildset ", arguments);
            var buildset = new projects.models.Buildset({number: number});
            var view = new projects.views.BuildsetDetails({model: buildset});
            var self = this;
            buildset.fetch({
                success: function () {
                    self.contentRegion.show(view);
                    zeus.navigate(buildset.get('url'));
                }
            });
        },

        showBuild: function (name, buildsetNumber, number) {
            console.log(" => show build", arguments);
        }
    });

    // We need to initialize controller before initialization so router can
    // trigger 'show:project' but we cannot do it before Project model is
    // defined
    // TODO: we can change order of how modules are loaded and put app.js 
    // at the end of this chain
    zeus.on('initialize:before', function () {
        var controller = new projects.Controller({
            region: region,
            project: new projects.models.Project(zeus.project)
        });

        zeus.on('show:project', controller.showProject);
        zeus.on('show:buildset', controller.showBuildset);
        zeus.on('show:build', controller.showBuild);

        projects.controller = controller;
    });

}, zeus.mainRegion, _, Marionette);
