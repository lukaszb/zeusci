from monolith.cli import SimpleExecutionManager
from monolith.cli import SingleLabelCommand


class InitCommand(SingleLabelCommand):

    def handle_label(self, label, namespace):
        print(" => zci init %r | %s" % (label, namespace))
        print(" => this is just a stub ...")


def main():
    app = SimpleExecutionManager('zci', commands={
        'init': InitCommand,
    })
    app.execute()

