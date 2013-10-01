
zeus = angular.module('zeus', ['ngResource', 'ui.router', 'zeusConstants', 'zeusFilters'])

zeus.run ($rootScope, $state, $stateParams, $http) ->
    """
    Always inject $state and $stateParams into the scope.
    """
    $rootScope.$state = $state
    $rootScope.$stateParams = $stateParams

    # CSRF
    for method in ['post', 'put']
        $http.defaults.headers[method]['X-CSRFToken'] = csrfToken
        $http.defaults.headers[method]['X-CSRFToken'] = csrfToken

zeus.config(($routeProvider, $locationProvider, $stateProvider, $urlRouterProvider) ->

    $urlRouterProvider.otherwise(PROJECT_URL)

    $stateProvider
        .state('project', {
            url: "#{PROJECT_URL}",
            views: {
                mainContent: {
                    controller: "ProjectDetailController",
                    templateUrl: "#{PARTIALS_URL}project_detail.html",
                },
            },
        })
        .state('build', {
            url: "#{PROJECT_URL}/buildsets/:buildsetNo.:buildNo/",
            views: {
                mainContent: {
                    controller: "BuildDetailController",
                    templateUrl: "#{PARTIALS_URL}build_detail.html",
                },
            },
        })
        .state('buildset', {
            url: "#{PROJECT_URL}/buildsets/:buildsetNo/",
            views: {
                mainContent: {
                    controller: "BuildsetDetailController",
                    templateUrl: "#{PARTIALS_URL}buildset_detail.html",
                },
            },
        })

    $locationProvider.html5Mode(true)
)

# bind app module object to window so other modules can reference it
@.zeus = zeus

