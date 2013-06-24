
$(function () {

    var showMessage = function (event) {
        console.log(event);
        $('#logs').append(event + '');
    };

    var socket = io.connect('/zeus')
    socket.on('connect', function () {
        console.log(' --> Connected to websocked');
    });
    socket.on('message', showMessage);

    socket.emit('connect', {
        name: PROJECT_NAME,
        build_no: BUILD_NO,
        step_no: STEP_NO,
    });

    socket.on('foo', showMessage);
    socket.on('output', function (data) {
        $('#output').text(data);
    });

    window.socket = socket;
});

