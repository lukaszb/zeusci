
zeus.POLL_INTERVAL = 3000

zeus.StepController = ($scope, $http, $timeout) ->

    init = () ->
        poll()

    fetch = (callback) ->
        $http.get(API_STEP_URL).success( (data) ->
            $scope.build = data;
            if callback
                callback()
        )

    poll = () ->
        callback = ->
            $timeout(poll, zeus.POLL_INTERVAL)
        fetch(callback)

    init()

zeus.StepController.$inject = ['$scope', '$http', '$timeout'];


zeus.ProjectDetailController = ($scope, $http, $timeout) ->

    init = () =>
        @.poll()



zeus.ProjectDetailController.$inject = ['$scope', '$http', '$timeout'];
