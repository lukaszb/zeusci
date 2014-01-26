zeus.simpleModule('apps.projects', function (projects, region) {

    var showProject = function () {
        console.log(" => show project");
        var view = new projects.views.ProjectDetails();
        region.show(view);
    }

    zeus.on('start', showProject);
}, zeus.mainRegion);
