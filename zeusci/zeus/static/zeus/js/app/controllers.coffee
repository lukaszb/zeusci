

zeus.controller 'ProjectController', ($scope, $timeout, Project) ->
    console.log " => init ProjectController"

    $scope.init = () ->
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
    Buildset.get routeParams, (buildset) ->
        $scope.buildset = buildset


zeus.controller 'BuildDetailController', ($scope, $stateParams, $timeout, Build) ->
    console.log " => init BuildDetailController"
    POLL_INTERVAL = 200
    controller = this

    routeParams = {
        name: $scope.project.name, # TODO: should not read from scope
        buildsetNo: $stateParams.buildsetNo,
        buildNo: $stateParams.buildNo,
    }

    $scope.forceRebuild = (build) ->
        build.$put routeParams, () ->
            # start polling again
            controller.poll()

    controller.shouldPoll = () ->
        return not $scope.build or not $scope.build.finished_at

    controller.poll = () ->
        if not controller.shouldPoll()
            return
        Build.get routeParams, (build) ->
            $scope.build = build
            $timeout(controller.poll, POLL_INTERVAL)

    Build.get routeParams, (build) ->
        $scope.build = build
        $timeout(controller.poll, POLL_INTERVAL)

