

zeus.controller 'ProjectController', ($scope, $timeout, Project) ->
    console.log " => init ProjectController"

    $scope.project = Project.getInstance()


zeus.controller 'ProjectDetailController', ($scope) ->
    console.log " => init ProjectDetailController"


zeus.controller 'BuildsetDetailController', ($scope, $routeParams, Buildset) ->
    console.log " => init BuildsetDetailController"

    routeParams = {
        name: $scope.project.name,
        buildsetNo: $routeParams.buildsetNo,
    }
    Buildset.query routeParams, (buildset) ->
        $scope.buildset = buildset


zeus.controller 'BuildDetailController', ($scope, $routeParams, $timeout, Build) ->
    # TODO: buildset is not preserved at this controller's scope
    console.log " => init BuildDetailController"

    routeParams = {
        name: $scope.project.name,
        buildsetNo: $routeParams.buildsetNo,
        buildNo: $routeParams.buildNo,
    }

    poll = () ->
        inner = () ->
            console.log "  => Polling build"
            Build.query routeParams, (build) ->
                $scope.build = build
        inner()
        $timeout(poll, 200)
    poll()

