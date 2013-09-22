
zeusFilters = angular.module('zeusFilters', [])
zeusFilters.filter('statusToBadgeClass', () ->
    filter = (text) ->
        switch text
            when zeus.status.PENDING then 'warning'
            when zeus.status.PASSED then 'success'
            when zeus.status.FAILED then 'important'
            else 'info'
    return filter
)
zeusFilters.filter('statusToClass', () ->
    filter = (text) ->
        switch text
            when zeus.status.PENDING then 'warning'
            when zeus.status.PASSED then 'success'
            when zeus.status.FAILED then 'error'
            else 'info'
    return filter
)

zeusFilters.filter('breadcrumbLinks', () ->
    filter = (breadcrumbs) ->
        return breadcrumbs.slice(0, breadcrumbs.length - 1)
)

zeusFilters.filter('breadcrumbActive', () ->
    filter = (breadcrumbs) ->
        if breadcrumbs.length > 0
            return [breadcrumbs[breadcrumbs.length - 1]]
        return breadcrumbs
)


@.zeus = angular.module('zeus', ['zeusFilters', 'ngResource'])
zeus.POLL_PROJECT = false # app should explictly tell if project polling is needed
zeus.status = {
    PENDING: 'pending',
    PASSED: 'passed',
    FAILED: 'failed',
}

zeus.config(['$routeProvider', '$locationProvider', ($routeProvider, $locationProvider) ->
    # There should be PROJECT_URL defined at the global scope
    TEMPLATES_URL = "/static/zeus/templates"
    #if PROJECT_URL[PROJECT_URL.length - 1] == "/"
        #PROJECT_URL = ""#PROJECT_URL.slice(0, PROJECT_URL.length - 1)

    zeus.API_PROJECT_DETAIL_URL = '/api/projects/:name.json'
    zeus.API_BUILDSET_DETAIL_URL = '/api/projects/:name/buildsets/:buildsetNo.json'
    zeus.API_BUILD_DETAIL_URL = '/api/projects/:name/builds/:buildsetNo.:buildNo.json'

    $routeProvider
        .when("#{PROJECT_URL}", {
            templateUrl: "#{TEMPLATES_URL}/project_detail.html",
            controller: "ProjectDetailController"})
        .when("#{PROJECT_URL}buildset/:buildsetNo/", {
            templateUrl: "#{TEMPLATES_URL}/buildset_detail.html",
            controller: "BuildsetDetailController"})
        .otherwise({redirectTo: PROJECT_URL})

    console.log "#{PROJECT_URL}buildsets/:buildsetNo"

    $locationProvider.html5Mode(true)
])

