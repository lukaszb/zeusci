
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

