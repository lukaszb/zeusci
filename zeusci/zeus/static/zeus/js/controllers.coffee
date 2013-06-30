
zeus.POLL_INTERVAL = 500

zeus.StepController = ($scope, $http, $timeout) ->

    init = () ->
        poll()

    fetch = (callback) ->
        $http.get(API_STEP_URL).success( (data) ->
            $scope.step = data;
            if callback
                callback()
        )

    poll = () ->
        callback = ->
            $timeout(poll, zeus.POLL_INTERVAL)
        fetch(callback)

    init()

zeus.StepController.$inject = ['$scope', '$http', '$timeout'];

