

zeus.controller 'ProjectController', ($scope, $timeout, Project) ->
    console.log " => init ProjectController"

    $scope.project = Project.getInstance()


zeus.controller 'ProjectBreadcrumbsController', ($scope, $state, $stateParams) ->
    project = $scope.project

    getBreadcrumbs = () ->
        buildsetNo = $stateParams.buildsetNo
        buildNo = $stateParams.buildNo

        breadcrumbs = [{name: $scope.project.name, url: $scope.project.url}]
        if $stateParams.buildsetNo
            url = $state.href('buildset', $stateParams)
            breadcrumbs.push {name: "Buildset ##{buildsetNo}", url: url}
        if $stateParams.buildNo
            url = $state.href('build', $stateParams)
            breadcrumbs.push {name: "Build ##{buildNo}", url: url}

        return breadcrumbs

    # we need to listen for success events, as at the beginning of state change
    # stateParams are still not updated
    $scope.$on '$stateChangeSuccess', () ->
        $scope.breadcrumbs = getBreadcrumbs()


zeus.controller 'ProjectDetailController', ($scope) ->
    console.log " => init ProjectDetailController"


zeus.controller 'BuildsetDetailController', ($scope, $routeParams, Buildset) ->
    console.log " => init BuildsetDetailController"

    routeParams = {
        name: $scope.project.name,
        buildsetNo: $scope.$stateParams.buildsetNo,
    }
    Buildset.query routeParams, (buildset) ->
        $scope.buildset = buildset


zeus.controller 'BuildDetailController', ($scope, $stateParams, $timeout, Build) ->
    # TODO: buildset is not preserved at this controller's scope
    console.log " => init BuildDetailController"

    routeParams = {
        name: $scope.project.name,
        buildsetNo: $stateParams.buildsetNo,
        buildNo: $stateParams.buildNo,
    }

    poll = () ->
        inner = () ->
            console.log "  => Polling build"
            Build.query routeParams, (build) ->
                $scope.build = build
        inner()
        $timeout(poll, 1500)
    poll()

