zeus.simpleModule('views', function (views, Marionette, $, swig) {
    zeus.views = zeus.views || {};

    zeus.views.View = Marionette.ItemView.extend({
        collectionContextName: 'items',
        serializeData: function () {
            var data = {};
            if (this.model) {
                data = this.model.toJSON();
            } else if (this.collection) {
                data[this.collectionContextName] = this.collection.toJSON();
            }
            return data;
        }

    });
}, Marionette, $, swig);
