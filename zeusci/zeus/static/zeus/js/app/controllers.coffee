

zeus.controller 'ProjectController', ($scope, $timeout, Project) ->
    console.log " => init ProjectController"

    $scope.project = Project.getInstance()


zeus.controller 'ProjectDetailController', ($scope) ->
    console.log " => init ProjectDetailController"

zeus.controller 'BuildsetDetailController', ($scope, $routeParams, Buildset) ->
    console.log " => init BuildsetDetailController"
    console.log $routeParams

    $scope.buildset = Buildset.query({
        name: $scope.project.name,
        buildsetNo: $routeParams.buildsetNo,
    })

