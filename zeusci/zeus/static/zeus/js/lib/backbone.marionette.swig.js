Backbone.Marionette.Renderer.render = function(template, data) {
    var html, templateFunc;
    if (typeof template === 'function') {
        templateFunc = swig.compile(template());
    } else {
        templateFunc = Marionette.TemplateCache.get(template);
    }
    html = templateFunc(data);
    return html;
};
Backbone.Marionette.TemplateCache.prototype.compileTemplate = function(rawTemplate) {
    return swig.compile(rawTemplate);
};