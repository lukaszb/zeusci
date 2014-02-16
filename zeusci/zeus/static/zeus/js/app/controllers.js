zeus.controller('ProjectDetailsController', function ($scope, project) {
    $scope.project = project;
});


zeus.controller('BreadcrumbsController', function ($scope, $state, $stateParams) {

    var getBreadcrumbs = function () {
        var breadcrumbs = [];

        var addBreadcrumb = function (name, url) {
            breadcrumbs.push({name: name, url: url});
        };

        // Project
        if ($stateParams.name) {
            var url = $state.href('project.details', $stateParams);
            addBreadcrumb($stateParams.name, url);
        }

        // Buildset
        if ($stateParams.buildsetNumber) {
            var name = "Buildset " + $stateParams.buildsetNumber;
            var url = $state.href('project.details.buildset', $stateParams);
            addBreadcrumb(name, url);
        }

        // Build
        if ($stateParams.buildNumber) {
            var name = [
                "Buildset ",
                $stateParams.buildsetNumber,
                ".",
                $stateParams.buildNumber
            ].join('');
            var url = $state.href('project.details.buildset.build', $stateParams);
            addBreadcrumb(name, url);
        }

        return breadcrumbs;
    }

    $scope.$on('$stateChangeSuccess', function () {
        $scope.breadcrumbs = getBreadcrumbs();
    });
});
