

zeus.controller 'ProjectController', ($scope, $timeout, $location, Project) ->
    console.log " => init ProjectController"

    $scope.project = Project.getInstance()


zeus.controller 'ProjectDetailController', ($scope, $location) ->
    console.log " => init ProjectDetailController"

zeus.controller 'BuildsetDetailController', ($scope, $location, $routeParams) ->
    console.log " => init BuildsetDetailController"

