zeus.controller('ProjectCreateController', function ($scope, Project) {

    $scope.project = {};
    var state = {processing: true};

    $scope.createProject = function () {
        state.processing = true;
        var project = new Project($scope.project);
        project.$post({name: ''}, function (obj) {
            state.processing = false;
            $scope.project = obj;  // TODO: API should return full object instead of empty one
        }, function (response) {
            $scope.errors = response.data;
            console.log(" -> Errors!: ", arguments);
        });
    };

});
