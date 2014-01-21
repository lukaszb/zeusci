(function (zeus, swig, _) {
    zeus.filters = zeus.filters || {};

    var status = zeus.constants.status;

    zeus.filters.statusToClass = function (text) {
        var map = {};
        map[status.PENDING] = 'warning';
        map[status.RUNNING] = 'primary';
        map[status.PASSED] = 'success';
        map[status.FAILED] = 'danger';
        if (map[text]) {
            return map[text];
        } else{
            return '';
        }
    };

    _.forEach(zeus.filters, function (filter, name) {
        swig.setFilter(name, filter);
    });
})(zeus, swig, _);
