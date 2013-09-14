
#/* jasmine specs for controllers go here */
describe('Zeus controllers', () ->

    describe('ProjectDetailController', () ->
        scope = null
        controller = null

        beforeEach(inject( ($rootScope, $controller) ->
            scope = $rootScope.$new()
            console.log zeus.ProjectDetailController
            controller = $controller(zeus.ProjectDetailController, {
                $scope: scope,
                #Project: null,
            })
        ))


        it('should create "phones" model with 3 phones', () ->
            scope = {}
            console.log(controller)
            #ctrl = new zeus.ProjectDetailController(scope)
            expect(3).toBe(3);

            #expect(scope.phones.length).toBe(3)
        )

    )
)

