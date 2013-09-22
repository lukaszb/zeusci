
zeus = angular.module('zeus', ['ngResource'])

zeus.config(['$routeProvider', '$locationProvider', ($routeProvider, $locationProvider) ->

    $routeProvider
        .when("#{PROJECT_URL}", {
            controller: "ProjectDetailController",
            templateUrl: "#{PARTIALS_URL}project_detail.html",
        })
        .when("#{PROJECT_URL}/buildsets/:buildsetNo", {
            controller: "BuildsetDetailController",
            templateUrl: "#{PARTIALS_URL}buildset_detail.html",
        })
        .otherwise({redirectTo: PROJECT_URL})

    $locationProvider.html5Mode(true)
])

# bind app module object to window so other modules can reference it
@.zeus = zeus

