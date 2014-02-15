zeus.filter('statusToClass', function (statuses) {
    var MAP = {};
    MAP[statuses.PENDING] = 'warning';
    MAP[statuses.RUNNING] = 'primary';
    MAP[statuses.PASSED] = 'success';
    MAP[statuses.FAILED] = 'danger';


    var filter = function (text) {
        var className = '';
        if (MAP[text] !== undefined) {
            className = MAP[text];
        }
        return className;
    };
    return filter;
});
