zeus.controller('BuildDetailsController', function ($scope, $stateParams, $timeout, Build) {

    $scope.forceRebuild = function () {
        $scope.build.$put($stateParams, function () {
            console.log(" -> PUT a build (forceRebuild)");
        });
    };

    var pollEnabled = true;

    function pollBuild () {

        function onBuildFetch (build) {
            $scope.build = build;
            if (pollEnabled) {
                $timeout(pollBuild, 250);
            }
        }

        Build.get($stateParams, onBuildFetch);
    }

    pollBuild();

    $scope.$on('$stateChangeStart', function () {
        // changeing out of this state, stop polling and allow garbage
        // collector to clean the controller
        pollEnabled = false;
    });

});
