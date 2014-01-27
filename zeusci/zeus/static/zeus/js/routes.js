zeus.simpleModule('routes', function (routes, Marionette, Backbone) {

    routes.Router = Marionette.AppRouter.extend({
        appRoutes: {
            "p/:name(/)": "showProject",
            "p/:name/buildsets/:buildsetNumber.:buildNumber(/)": "showBuild",
            "p/:name/buildsets/:buildsetNumber(/)": "showBuildset"
        }
    });

    routes.routerController = {
        showProject: function (name) {
            console.log(" --> router showProject:", name);
            zeus.trigger('show:project', name);
        },
        showBuildset: function (name, buildsetNumber) {
            console.log(" --> router showBuildset", name, buildsetNumber);
            zeus.trigger('show:buildset', name, buildsetNumber);
        },
        showBuild: function (name, buildsetNumber, buildNumber) {
            console.log(" --> router showBuild", name, buildsetNumber, buildNumber);
            zeus.trigger('show:build', name, buildsetNumber, buildNumber);
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
}, Marionette, Backbone);
