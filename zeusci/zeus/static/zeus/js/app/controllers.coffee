

zeus.controller 'ProjectController', ($scope, $timeout, Project) ->
    console.log " => init ProjectController"

    $scope.project = Project.getInstance()


zeus.controller 'ProjectDetailController', ($scope) ->
    console.log " => init ProjectDetailController"


zeus.controller 'BuildsetDetailController', ($scope, $routeParams, Buildset) ->
    console.log " => init BuildsetDetailController"

    routeParams = {
        name: $scope.project.name,
        buildsetNo: $scope.$stateParams.buildsetNo,
    }
    console.log routeParams
    Buildset.query routeParams, (buildset) ->
        console.log buildset
        $scope.buildset = buildset


zeus.controller 'BuildDetailController', ($scope, $stateParams, $timeout, Build) ->
    # TODO: buildset is not preserved at this controller's scope
    console.log " => init BuildDetailController"

    routeParams = {
        name: $scope.project.name,
        buildsetNo: $stateParams.buildsetNo,
        buildNo: $stateParams.buildNo,
    }

    poll = () ->
        inner = () ->
            console.log "  => Polling build"
            Build.query routeParams, (build) ->
                $scope.build = build
        inner()
        $timeout(poll, 1500)
    poll()

