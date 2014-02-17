zeus.controller('BuildDetailsController', function ($scope, $stateParams, $timeout, Build) {

    $scope.forceRebuild = function () {
        console.log(" -> forceRebuild: ", $scope.build.$resolved);
        window.build = $scope.build;
        build.$put($stateParams, function () {
            console.log(" -> PUT a build (forceRebuild)");
        });
    }

    (function pollBuild() {
        Build.get($stateParams, function (build) {
            console.log(" -> pollBuild");
            $scope.build = build;
            $timeout(pollBuild, 250);
        });
    })();

});
