zeus.simpleModule('routes', function (routes, Marionette, Backbone) {

    routes.api = {
        getProjectUrl: function () {
            return zeus.project.uri;
        },
        getBuildsetUrl: function (number) {
            var projectUrl = this.getProjectUrl();
            return projectUrl + '/buildsets/' + number;
        }
    }

    routes.Router = Marionette.AppRouter.extend({
        appRoutes: {
            "": "showProject",
            "buildsets/:buildsetNumber": "showBuildset"
        }
    });

    routes.routerController = {
        showProject: function () {
            console.log(" --> router show project");

        },
        showBuildset: function () {
            console.log(" --> router show buildset");
        }
    };

    zeus.addInitializer(function () {
        routes.router = new routes.Router({
            controller: routes.routerController
        });
    });

    zeus.on('initialize:after', function () {
        Backbone.history.start({pushState: true});
    });

    zeus.on('start', function () {
        console.log("app routes started");
        var project = zeus.request('project');
        var buildset = zeus.request('buildset');
    });

}, Marionette, Backbone);
