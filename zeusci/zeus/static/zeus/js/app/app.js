zeus = (function (angular) {
    var zeus = angular.module('zeus', ['ngResource', 'ngCookies', 'ui.router', 'ui.bootstrap']);

    zeus.run(function ($http, $cookies, $rootScope, $stateParams) {
        // Always set $stateParams at the scope
        $rootScope.$stateParams = $stateParams;

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
                url: '/p/{name}',
                resolve: {
                    project: function (Project, $stateParams) {
                        console.log(" -> Resolving Project " + $stateParams.name);
                        return Project.get({name: $stateParams.name});
                    }
                },
                templateUrl: resolveTemplate('project.wrapper'),
                onEnter: function (Project, Buildset) {
                    // put services as deps so they are actually resolved
                    console.log(" => onEnter: project");
                }
            })
            .state('project.details', {
                url: '',
                onEnter: function () {
                    console.log(" => onEnter: project.details");
                },
                views: {
                    // injects into unnamed ui-view in parent's state
                    '': {
                        templateUrl: resolveTemplate('project.details'),
                        controller: 'ProjectDetailsController'
                    },
                    // injects into 'project-content' ui-view in parent's state
                    'project-content': {
                        templateUrl: resolveTemplate('buildset.list'),
                        controller: 'ProjectDetailsController'
                    }
                }
            })
            .state('project.details.createBuildset', {
                url: '/buildsets/init',
                views: {
                    // injects into parent's ui-view ('project-content')
                    '': {
                        templateUrl: resolveTemplate('buildset.create'),
                        controller: 'BuildsetCreateController'
                    }
                }
            })
            .state('project.details.buildset', {
                url: '/buildsets/{buildsetNumber:[0-9]{1,}}',
                views: {
                    // injects into parent's ui-view ('project-content')
                    '': {
                        templateUrl: resolveTemplate('buildset.details'),
                        controller: function ($scope, $stateParams, Buildset) {
                            $scope.buildset = Buildset.get($stateParams);
                            console.log(" => project.details.buildset | view: ''");
                        }
                    }
                },
                onEnter: function () {
                    console.log(" => onEnter: project.details.buildset");
                }
            })
            .state('project.details.buildset.build', {
                url: '.{buildNumber:[0-9]{1,}}',
                views: {
                    'project-content@project': {
                        templateUrl: resolveTemplate('build.details'),
                        controller: function ($scope, $stateParams, Build) {
                            console.log(" => project.details.buildset.build | view: ''");
                            $scope.build = Build.get($stateParams);
                        }
                    }
                },
                onEnter: function () {
                    console.log(" => onEnter: project.details.buildset.build");
                }
            })
        ;

        $locationProvider.html5Mode(true)
    });

    return zeus;
})(angular);
