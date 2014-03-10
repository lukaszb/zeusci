zeus.controller('BuildsetCreateController', function ($scope, $stateParams, Buildset) {
    var state = {};

    $scope.initController = function () {
        $scope.newBuildset = {};
        state.processing = true;
    };

    $scope.createBuildset = function () {
        state.processing = true;
        var buildset = new Buildset($scope.newBuildset);
        buildset.$post($stateParams, function (obj) {
            state.processing = false;
            $scope.buildset = obj;  // TODO: API should return full object instead of empty one
        }, function (response) {
            // TODO: Handle errors
        });
    };
});
