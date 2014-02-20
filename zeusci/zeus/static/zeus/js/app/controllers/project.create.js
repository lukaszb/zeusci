zeus.controller('ProjectCreateController', function ($scope, $state, Project) {

    $scope.project = {};
    var state = {processing: true};

    $scope.createProject = function () {
        state.processing = true;
        var project = new Project($scope.project);
        project.$post({name: ''}, function (obj) {
            state.processing = false;
            $scope.project = obj;  // TODO: API should return full object instead of empty one
            $state.go('project.details', {name: obj.name});
        }, function (response) {
            $scope.errors = response.data;
            console.log(" -> Errors!: ", arguments);
        });
    };

});
