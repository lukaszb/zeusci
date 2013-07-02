
zeusFilters = angular.module('zeusFilters', [])
zeusFilters.filter('statusToClass', () ->
    filter = (text) ->
        switch text
            when zeus.status.PENDING then 'warning'
            when zeus.status.PASSED then 'success'
            when zeus.status.FAILED then 'important'
            else 'info'
    return filter
)


@.zeus = angular.module('zeus', ['zeusFilters', 'ngResource'])
zeus.POLL_PROJECT = false # app should explictly tell if project polling is needed
zeus.status = {
    PENDING: 'pending',
    PASSED: 'passed',
    FAILED: 'failed',
}

