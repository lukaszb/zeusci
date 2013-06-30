

console.log "Loaded coffee-script"
console.log "#{API_STEP_URL}"

window.StepController = ($scope, $http, $timeout) ->

    fetch = (callback) ->
        $http.get(API_STEP_URL).success( (data) ->
            $scope.step = data;
            if callback
                callback()
        )

    tick = () ->
        fetch( ->
            $timeout(tick, 500)
        )
    tick()
