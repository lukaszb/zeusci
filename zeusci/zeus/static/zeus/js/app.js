(function (Backbone, zeus_project) {

    var ZeusApp = Backbone.View.extend({
        initialize: function (options) {
            this.project = options.project;
        },

        start: function () {
            this.trigger('start');
            return this;
        }
    });

    this.zeus = new ZeusApp({project: zeus_project});
    //this.zeus.on('start', function () {
        //console.log("zeusApp started!");
    //});
    this.zeus.start();

})(Backbone, zeus_project);
