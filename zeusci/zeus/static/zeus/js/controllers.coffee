
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


zeus.controller('BuildsetDetailController', ($scope, $timeout, Buildset) ->
    zeus.POLL_PROJECT = false
    controller = this


    $scope.init = (buildset_json) ->
        $scope.buildset = JSON.parse(buildset_json)
        $scope.breadcrumbs.push(controller.getBreadcrumb())
        $timeout(controller.poll, zeus.POLL_INTERVAL)

    controller.getBreadcrumb = () ->
        url = $scope.buildset.url
        text = "Buildset ##{$scope.buildset.number}"
        return {url: url, text: text}


    controller.shouldPoll = () ->
        return zeus.POLL_ENABLED and not $scope.buildset.finished_at

    controller.poll = () ->
        if not controller.shouldPoll()
            return
        console.log " => poll buildset"
        project = $scope.project
        buildset = $scope.buildset
        Buildset.get({name: project.name, buildsetNo: buildset.number}, (buildset) ->
            $scope.buildset = buildset
            $timeout(controller.poll, zeus.POLL_INTERVAL)
        )

)


zeus.controller('BuildDetailController', ($scope, $timeout, Build) ->
    zeus.POLL_PROJECT = false
    controller = this

    $scope.init = () ->
        $scope.build = Build.getInitialBuild()
        $scope.breadcrumbs.push(controller.getBreadcrumb())
        $timeout(controller.poll, zeus.POLL_BUILD_INTERVAL)
        if window.force_build_url
            $scope.force_build_url = force_build_url

    controller.getBreadcrumb = () ->
        url = $scope.build.url
        text = "Build ##{$scope.build.number}"
        return {url: url, text: text}

    controller.shouldPoll = () ->
        should = zeus.POLL_ENABLED and not $scope.build.finished_at
        return should

    controller.poll = () ->
        if not controller.shouldPoll()
            return
        console.log " => poll build"
        params = {
            name: $scope.project.name,
            buildsetNo: $scope.buildset.number,
            buildNo: $scope.build.number,
        }
        Build.get(params, (build) ->
            $scope.build = build
            $timeout(controller.poll, zeus.POLL_BUILD_INTERVAL)
        )

)

