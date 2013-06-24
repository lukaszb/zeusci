import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from socketio.sdjango import namespace

from .models import BuildStep


@namespace('/zeus')
class BuildStepNamespace(BaseNamespace, BroadcastMixin):
    nicknames = []

    def initialize(self):
        self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started: /zeus")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_nickname(self, nickname):
        self.log('Nickname: {0}'.format(nickname))
        self.nicknames.append(nickname)
        self.socket.session['nickname'] = nickname
        self.broadcast_event('announcement', '%s has connected' % nickname)
        self.broadcast_event('nicknames', self.nicknames)
        return True, nickname

    def on_foo(self, data):
        self.log(repr(data))

    def on_connect(self, data):
        self.log('connected: %r' % str(data))
        # TODO: Check user data!
        filters = {
            'build__project__name': data['name'],
            'build__number': data['build_no'],
            'number': data['step_no'],
        }
        step = BuildStep.objects.get(**filters)
        self.log("BuildStep: %s" % step)
        # Stream output
        import gevent
        output = ''
        while step.finished_at is None:
            new_output = step.output
            if len(new_output) > len(output):
                self.emit('output', step.output)
            sleep = 0.1
            self.log("Sleeping websocket for %s" % sleep)
            gevent.sleep(sleep)
        self.emit('output', step.output)

    def recv_disconnect(self):
        # Remove nickname from the list.
        self.log('Disconnected')
        #nickname = self.socket.session['nickname']
        #self.nicknames.remove(nickname)
        self.broadcast_event('announcement', '%s has disconnected' % nickname)
        self.broadcast_event('nicknames', self.nicknames)
        self.disconnect(silent=True)
        return True

