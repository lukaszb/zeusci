
zeus.POLL_ENABLED = true
zeus.POLL_INTERVAL = 3000
zeus.POLL_BUILD_INTERVAL = 300


zeus.controller('ProjectDetailController', ($scope, $timeout, Project) ->
    @.POLL_PROJECT = true
    controller = this

    $scope.init = (project) ->
        project = JSON.parse(project)
        $scope.project = project
        $scope.breadcrumbs = [{url: $scope.project.url, text: $scope.project.name}]
        $timeout(controller.poll, zeus.POLL_INTERVAL)

    controller.poll = () ->
        if not controller.shouldPoll()
            return
        console.log " => poll project"
        Project.get({name: $scope.project.name}, (project) ->
            $scope.project = project
            $timeout(controller.poll, zeus.POLL_INTERVAL)
        )

    controller.shouldPoll = () ->
        return zeus.POLL_ENABLED and @.POLL_PROJECT

)


zeus.BuildsetDetailController = ($scope, $timeout, Buildset) ->
    window.Buildset = Buildset
    console.log " => Init BuildsetDetailController"
    zeus.POLL_PROJECT = false

    $scope.buildset = zeus_buildset

    getBreadcrumb = () ->
        url = $scope.buildset.url
        text = "Buildset ##{$scope.buildset.number}"
        return {url: url, text: text}

    $scope.breadcrumbs.push(getBreadcrumb())

    shouldPoll = () ->
        return zeus.POLL_ENABLED and not $scope.buildset.finished_at

    poll = () ->
        if not shouldPoll()
            return
        console.log " => poll buildset"
        project = $scope.project
        buildset = $scope.buildset
        Buildset.get({name: project.name, buildsetNo: buildset.number}, (buildset) ->
            $scope.buildset = buildset
            $timeout(poll, zeus.POLL_INTERVAL)
        )

    $timeout(poll, zeus.POLL_INTERVAL)


zeus.BuildsetDetailController.$inject = ['$scope', '$timeout', 'Buildset']


zeus.BuildDetailController = ($scope, $timeout, Build) ->
    console.log " => Init BuildDetailController"
    zeus.POLL_PROJECT = false

    $scope.build = zeus_build

    getBreadcrumb = () ->
        url = $scope.build.url
        text = "Build ##{$scope.build.number}"
        return {url: url, text: text}
    $scope.breadcrumbs.push(getBreadcrumb())

    shouldPoll = () ->
        should = zeus.POLL_ENABLED and not $scope.build.finished_at
        return should

    poll = () ->
        if not shouldPoll()
            return
        console.log " => poll build"
        project = zeus_project
        buildset = zeus_buildset
        build = zeus_build
        params = {name: project.name, buildsetNo: buildset.number, buildNo: build.number}
        Build.get(params, (build) ->
            $scope.build = build
            $timeout(poll, zeus.POLL_BUILD_INTERVAL)
        )

    $timeout(poll, zeus.POLL_BUILD_INTERVAL)

    if window.force_build_url
        $scope.force_build_url = force_build_url

zeus.BuildDetailController.$inject = ['$scope', '$timeout', 'Build']

