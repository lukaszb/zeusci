(function (project) {

    zeus.constant('settings', {
        API_PROJECT_URL: '/api/projects/:name'
    });


    zeus.factory('Project', function ($resource, settings) {
        var Project = $resource(settings.API_PROJECT_URL, {name: '@name'});
        Project.getInstance = function () {
            return project;
        };
        zeus.Project = Project;  // TODO: Remove me
        return Project;
    });

})(project);
