zeus.module("Controllers", function (Controllers, App, Backbone, Marionette, $, _) {

    Controllers.Controller = Marionette.Controller.extend({
        initialize: function (options) {
            this.region = (options || {}).region;
            Marionette.Controller.prototype.initialize.call(this, options);
        },

        show: function (view) {
            this.region.show(view);
        }

    });
})
