zeus.simpleModule('apps.projects.views', function (views, Marionette, $) {

    views.ProjectLayout = Marionette.Layout.extend({
        template: "#project-layout-template",

        regions: {
            contentRegion: "#project-content-region"
        }
    });


    var navigateOnClick = function (event) {
        var url = $(event.target).attr('href');
        if (url && url[0] === '/') {
            event.preventDefault();
            event.stopPropagation();
            zeus.navigate(url, {trigger: true});
        }
    }


    views.ProjectDetails = zeus.views.View.extend({
        template: "#project-details-template",
        modelContextName: "project",

        events: {
            "click a": navigateOnClick
        }
    });


    views.BuildsetDetails = zeus.views.View.extend({
        template: "#buildset-details-template",
        modelContextName: "buildset",

        events: {
            "click a": navigateOnClick
        }
    });


    views.BuildDetails = zeus.views.View.extend({
        template: "#build-details-template",
        modelContextName: "build"
    });

}, Marionette, $);
