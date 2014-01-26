zeus.simpleModule('views', function (views, Marionette, $, swig) {
    zeus.views = zeus.views || {};

    zeus.views.View = Marionette.ItemView.extend({
        collectionContextName: 'items',
        modelContextName: null,

        initialize: function () {
            Marionette.ItemView.prototype.initialize.apply(this, arguments);
            if (this.collection) {
                this.collection.on('reset', this.render);
            }
        },

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
