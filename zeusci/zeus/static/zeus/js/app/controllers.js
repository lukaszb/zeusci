zeus.controller('ProjectDetailsController', function ($scope, project) {
    $scope.project = project;
});


zeus.controller('BreadcrumbsController', function ($scope, $state, $stateParams) {

    var getBreadcrumbs = function () {
        var breadcrumbs = [];

        var addBreadcrumb = function (name, url) {
            breadcrumbs.push({name: name, url: url});
        };

        if ($stateParams.name) {
            var url = $state.href('project.details', $stateParams);
            addBreadcrumb($stateParams.name, url);
        }

        if ($stateParams.buildsetNumber) {
            var name = "Buildset #" + $stateParams.buildsetNumber;
            var url = $state.href('project.details.buildset', $stateParams);
            addBreadcrumb(name, url);
        }

        return breadcrumbs;
    }

    $scope.$on('$stateChangeSuccess', function () {
        $scope.breadcrumbs = getBreadcrumbs();
    });
});
