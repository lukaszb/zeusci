(function (project) {

    zeus.constant('settings', {
        API_PROJECT_URL: '/api/projects/:name',
        API_BUILDSET_URL: '/api/projects/:name/buildsets/:buildsetNumber',
        API_BUILD_URL: '/api/projects/:name/builds/:buildsetNumber.:buildNumber',
    });


    zeus.factory('Project', function ($resource, settings) {
        var Project = $resource(settings.API_PROJECT_URL, {name: '@name'});
        Project.getInstance = function () {
            return project;
        };
        zeus.Project = Project;  // TODO: Remove me
        return Project;
    });


    zeus.factory('Buildset', function ($resource, settings) {
        var Buildset = $resource(settings.API_BUILDSET_URL, {}, {
            post: {method: 'POST'}
        });
        zeus.Buildset = Buildset;  // TODO Remove me
        return Buildset;
    });


    zeus.factory('Build', function ($resource, settings) {
        var Build = $resource(settings.API_BUILD_URL, {}, {
            put: {method: 'PUT'}
        });
        zeus.Build = Build;  // TODO Remove me
        return Build;
    });
})(project);
