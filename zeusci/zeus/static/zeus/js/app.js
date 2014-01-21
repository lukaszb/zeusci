(function (Marionette) {
    var zeus = new Marionette.Application();

    zeus.addRegions({
        mainRegion: "#main-region",
        breadcrumbsRegion: "#breadcrumbs-region",
    })

    window.zeus = zeus;
})(Marionette);
