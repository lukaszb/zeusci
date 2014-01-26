zeus.simpleModule('apps.projects', function (projects, region) {

    controller = {
        showProject: function () {
            console.log(" => show project");
            var view = new projects.views.ProjectDetails({
                model: new projects.models.Project(zeus.project)
            });
            region.show(view);
        },

        showBuildset: function (name, number) {
            console.log(" => show buildset " + number);
            var buildset = new projects.models.Buildset({number: number});
            var view = new projects.views.BuildsetDetails({model: buildset});
            buildset.fetch({
                success: function () {
                    region.show(view);
                    zeus.navigate(buildset.get('url'));
                }
            });
        }
    };

    zeus.on('show:project', controller.showProject);
    zeus.on('show:buildset', controller.showBuildset);

}, zeus.mainRegion);
