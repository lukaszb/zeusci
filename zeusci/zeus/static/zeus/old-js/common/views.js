zeus.module("Views", function (Views, Appa, Backbone, Marionette, $, _) {

    Views.ItemView = Marionette.ItemView.extend({
        contextCollectionName: 'items',

        serializeData: function () {
            var data = {};
            if (this.model) {
                data = this.model.toJSON();
            } else if (this.collection) {
                data[this.contextCollectionName] = this.collection.toJSON();
            }
            return data;
        }
    });
});
