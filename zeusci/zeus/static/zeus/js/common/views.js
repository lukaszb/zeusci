(function (zeus, Backbone, $, swig) {
    zeus.views = zeus.views || {};

    zeus.views.View = Backbone.View.extend({
        getTemplateHtml: function () {
            return $(this.template).html();
        },

        getTemplate: function () {
            if (this._cachedTemplate === undefined) {
                var templateHtml = this.getTemplateHtml();
                this._cachedTemplate = swig.compile(templateHtml);
            }
            return this._cachedTemplate;
        },

        getContextData: function () {
            return {};
        },

        render: function () {
            var context = this.getContextData();
            var template = this.getTemplate();
            this.$el.empty().html(template)
            return this;
        }
    });
})(zeus, Backbone, $, swig);
