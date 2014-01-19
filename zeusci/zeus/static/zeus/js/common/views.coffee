@zeus.module "Views", (Views, Appa, Backbone, Marionette, $, _) ->


    class Views.ItemView extends Marionette.ItemView
        contextCollectionName: 'items'

        serializeData: ->
            data = {}
            if this.model
                data = this.model.toJSON()
            else if this.collection
                data[@contextCollectionName] = this.collection.toJSON()
            return data
