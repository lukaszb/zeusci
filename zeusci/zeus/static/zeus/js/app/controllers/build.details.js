zeus.controller('BuildDetailsController', function ($scope, $stateParams, $timeout, Build) {

    $scope.forceRebuild = function () {
        $scope.build.$put($stateParams, function () {
            console.log(" -> PUT a build (forceRebuild)");
        });
    };

    (function pollBuild() {
        Build.get($stateParams, function (build) {
            console.log(" -> pollBuild");
            $scope.build = build;
            $timeout(pollBuild, 250);
        });
    })();

});
