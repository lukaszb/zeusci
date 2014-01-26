zeus.simpleModule('apps.projects', function (projects, region) {

    controller = {
        showProject: function () {
            console.log(" => show project");
            var view = new projects.views.ProjectDetails({
                model: new projects.models.Project(zeus.project)
            });
            view.on('buildset:show', controller.showBuildset);
            region.show(view);
        },

        showBuildset: function (number) {
            console.log(" => show buildset " + number);
            var buildset = new projects.models.Buildset({number: number});
            var view = new projects.views.BuildsetDetails({model: buildset});
            buildset.fetch({
                success: function () {
                    region.show(view);
                }
            });
        }
    };

    zeus.on('start', controller.showProject);
    zeus.on('buildset:show', controller.showBuildset)
}, zeus.mainRegion);
