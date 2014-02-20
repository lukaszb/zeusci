zeus.controller('ProjectDetailsController', function ($scope, project) {
    $scope.project = project;
});


zeus.controller('BreadcrumbsController', function ($scope, $state, $stateParams) {

    var getBreadcrumbs = function () {
        var breadcrumbs = [];
        var name, url;

        var addBreadcrumb = function (name, url) {
            breadcrumbs.push({name: name, url: url});
        };

        // Project List
        url = $state.href('project.list');
        addBreadcrumb("Projects", url);

        if ($state.current.name === 'project.create') {
            addBreadcrumb('New', '#');
        }

        // Project
        if ($stateParams.name) {
            url = $state.href('project.details', $stateParams);
            addBreadcrumb($stateParams.name, url);
        }

        // Buildset
        if ($stateParams.buildsetNumber) {
            name = "Buildset " + $stateParams.buildsetNumber;
            url = $state.href('project.details.buildset', $stateParams);
            addBreadcrumb(name, url);
        }

        // Build
        if ($stateParams.buildNumber) {
            name = [
                "Buildset ",
                $stateParams.buildsetNumber,
                ".",
                $stateParams.buildNumber
            ].join('');
            url = $state.href('project.details.buildset.build', $stateParams);
            addBreadcrumb(name, url);
        }

        return breadcrumbs;
    }

    $scope.$on('$stateChangeSuccess', function () {
        $scope.breadcrumbs = getBreadcrumbs();
    });
});


zeus.controller('BuildsetCreateController', function ($scope, $stateParams, Buildset) {
    var state = {};

    $scope.initController = function () {
        $scope.newBuildset = {};
        state.processing = true;
    }

    $scope.createBuildset = function () {
        state.processing = true;
        var buildset = new Buildset($scope.newBuildset);
        buildset.$post($stateParams, function (obj) {
            state.processing = false;
            $scope.buildset = obj;  // TODO: API should return full object instead of empty one
        }, function () {
            console.log(" -> Errors!: ", arguments);
        });
    }
});
