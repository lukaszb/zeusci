(function (Marionette, zeus_project) {

    var ZeusApp = Marionette.Application.extend({
        initialize: function (options) {
            this.project = options.project;
            delete options.project;
            Marionette.Application.prototype.call(this, arguments);
        },

        simpleModule: function (moduleNames, moduleDefinition) {
            var args = Array.prototype.slice.call(arguments);
            var self = this;

            // wrapper would receive module as first argument
            // any extra arguments must be explicitly passed to simpleModule
            // arguments
            args[1] = function moduleDefinitionWrapper () {
                var wrapperArgs = Array.prototype.slice.call(arguments);
                // only pass explicit arguments
                var newArgs = wrapperArgs.slice(6);
                // and include only module definition as first argument
                newArgs.unshift(wrapperArgs[0]);
                return moduleDefinition.apply(self, newArgs);
            }
            Marionette.Application.prototype.module.apply(this, args);
        }
    });

    zeus = new ZeusApp({project: zeus_project});

    zeus.addRegions({
        breadcrumbsRegion: "#breadcrumbs-region",
        mainRegion: "#main-region"
    });

    window.zeus = zeus;
    // start app when all js/templates are loaded
})(Marionette, zeus_project);
