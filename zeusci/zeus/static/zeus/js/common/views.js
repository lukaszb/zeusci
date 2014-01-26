zeus.simpleModule('views', function (views, Marionette, $, swig) {
    zeus.views = zeus.views || {};

    zeus.views.View = Marionette.ItemView.extend({
        collectionContextName: 'items',
        modelContextName: null,

        serializeData: function () {
            var data = {};
            if (this.model) {
                var modelData = this.model.toJSON();
                if (this.modelContextName) {
                    data[this.modelContextName] = modelData;
                } else {
                    data = modelData;
                }
            } else if (this.collection) {
                data[this.collectionContextName] = this.collection.toJSON();
            }
            return data;
        }

    });
}, Marionette, $, swig);
