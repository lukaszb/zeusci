zeus = (function (angular) {
    var zeus = angular.module('zeus', ['ngResource', 'ngCookies', 'ui.router', 'ui.bootstrap']);

    zeus.run(function ($http, $cookies) {
        // Pass CSRF token from cookie to all data send back to the server
        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    });

    zeus.config(function ($locationProvider, $stateProvider, $urlRouterProvider) {

        var STATIC_URL = "/static/";
        var PARTIALS_URL = STATIC_URL + "zeus/js/app/partials/";

        var resolveTemplate = function (templateId) {
            return PARTIALS_URL + templateId + '.html';
        };

        $urlRouterProvider.otherwise('/');

        console.log(" => setting up the states");
        $stateProvider
            .state('project', {
                abstract: true,
                url: '/p/:name',
                resolve: {
                    project: function (Project, $stateParams) {
                        return Project.get({name: $stateParams.name});
                    }
                },
                template: '<ui-view/>',
                onEnter: function () {
                    console.log(" => onEnter: project");
                }
            })
            .state('project.details', {
                url: '',
                templateUrl: resolveTemplate('project.details'),
                controller: 'ProjectDetailsController',
                onEnter: function () {
                    console.log(" => onEnter: project.details");
                }
            })
        ;

        $locationProvider.html5Mode(true)
    });

    return zeus;
})(angular);
