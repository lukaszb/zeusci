
describe('Zeus controllers', () ->

    beforeEach(module('zeus'));

    describe('ProjectDetailController', () ->
        scope = null
        controller = null
        timeout = null

        beforeEach(inject( ($rootScope, $controller, $timeout) ->
            timeout = $timeout
            scope = $rootScope.$new()
            controller = $controller('ProjectDetailController', {
                $scope: scope,
                $timeout: timeout,
            })
        ))

        describe('.init', () ->
            project = {
                name: 'Tron',
                url: '/projects/1',
            }

            beforeEach(() ->
                controller.poll = () ->
                    scope.pollerWasStarted = true
                scope.init(JSON.stringify(project))
            )

            it('should properly set project', () ->
                expect(scope.project).toEqual(project)
            )

            it('should properly set breadcrumbs', () ->
                expect(scope.breadcrumbs).toEqual([
                    {url: project.url, text: project.name},
                ])
            )

            it('should run poller', () ->
                expect(scope.pollerWasStarted).toBe(undefined)
                timeout.flush()
                expect(scope.pollerWasStarted).toBe(true)
            )

        )

        it('.shouldPoll', () ->
            expect(controller.shouldPoll()).toBe(true)
            controller.POLL_PROJECT = false
            expect(controller.shouldPoll()).toBe(false)
        )

        it('.poll', () ->
            # TODO: Test polling
        )

    )

    describe('BuildsetDetailController', () ->
        scope = null
        controller = null
        timeout = null
        project = null

        beforeEach(inject( ($rootScope, $controller, $timeout) ->
            project = {
                name: 'Tron',
                url: '/projects/1',
            }
            timeout = $timeout
            scope = $rootScope.$new()
            scope.project = project
            scope.breadcrumbs = []
            controller = $controller('BuildsetDetailController', {
                $scope: scope,
                $timeout: timeout,
            })
        ))

        it('.getBreadcrumb', () ->
            scope.buildset = {number: 145, url: '/foo/bar'}
            scope.breadcrumbs = []
            breadcrumb = controller.getBreadcrumb()
            expect(breadcrumb).toEqual({url: '/foo/bar', text: 'Buildset #145'})
        )

        it('.shouldPoll', () ->
            scope.buildset = {}
            expect(controller.shouldPoll()).toBe(true)
            scope.buildset.finished_at = 'some date'
            expect(controller.shouldPoll()).toBe(false)
        )

    )
)

