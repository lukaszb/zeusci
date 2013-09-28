
zeus = angular.module('zeus', ['ngResource', 'ui.router', 'zeusConstants', 'zeusFilters'])

zeus.run ($rootScope, $state, $stateParams) ->
    $rootScope.$state = $state
    $rootScope.$stateParams = $stateParams

zeus.config(($routeProvider, $locationProvider, $stateProvider, $urlRouterProvider) ->

    $urlRouterProvider.otherwise(PROJECT_URL)

    $stateProvider
        .state('project', {
            url: "#{PROJECT_URL}",
            controller: "ProjectDetailController",
            templateUrl: "#{PARTIALS_URL}project_detail.html",
        })
        .state('build', {
            url: "#{PROJECT_URL}/buildsets/:buildsetNo.:buildNo/",
            controller: "BuildDetailController",
            templateUrl: "#{PARTIALS_URL}build_detail.html",
        })
        .state('buildset', {
            url: "#{PROJECT_URL}/buildsets/:buildsetNo/",
            controller: "BuildsetDetailController",
            templateUrl: "#{PARTIALS_URL}buildset_detail.html",
        })


    #$routeProvider
        #.when("#{PROJECT_URL}", {
            #controller: "ProjectDetailController",
            #templateUrl: "#{PARTIALS_URL}project_detail.html",
        #})
        #.when("#{PROJECT_URL}/buildsets/:buildsetNo.:buildNo/", {
            #controller: "BuildDetailController",
            #templateUrl: "#{PARTIALS_URL}build_detail.html",
        #})
        #.when("#{PROJECT_URL}/buildsets/:buildsetNo/", {
            #controller: "BuildsetDetailController",
            #templateUrl: "#{PARTIALS_URL}buildset_detail.html",
        #})
        #.otherwise({redirectTo: PROJECT_URL})

    $locationProvider.html5Mode(true)
)

# bind app module object to window so other modules can reference it
@.zeus = zeus

