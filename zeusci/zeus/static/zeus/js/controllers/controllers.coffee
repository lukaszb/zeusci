

zeus.controller("ProjectController", ($scope, $timeout, $location, Project) ->
    controller = this;

    $scope.init = (projectJSON) ->
        $scope.project = JSON.parse(projectJSON);
        $scope.breadcrumbs = [{url: $scope.project.url, text: $scope.project.name}]

);


zeus.controller("ProjectDetailController", ($scope, $timeout, $location, Project) ->
    controller = this;

);

