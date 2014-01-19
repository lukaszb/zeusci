@zeus.module "Controllers", (Controllers, Appa, Backbone, Marionette, $, _) ->


    class Controllers.Controller extends Marionette.Controller

        constructor: (options = {}) ->
            @region = options.region
            super options

        show: (view) ->
            @region.show view
