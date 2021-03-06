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
    };

    $scope.$on('$stateChangeSuccess', function () {
        $scope.breadcrumbs = getBreadcrumbs();
    });
});
