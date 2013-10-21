
zeusFilters = angular.module('zeusFilters', ['zeusConstants'])

zeusFilters.filter('statusToClass', () ->
    filter = (text) ->
        switch text
            when zeusConstants.status.PENDING then 'warning'
            when zeusConstants.status.RUNNING then 'primary'
            when zeusConstants.status.PASSED then 'success'
            when zeusConstants.status.FAILED then 'danger'
            else ''
    return filter
)

@.zeusFilters = zeusFilters

