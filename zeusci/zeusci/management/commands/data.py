from django.core.management.base import NoArgsCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from zeus.models import Project


User = get_user_model()


class Command(NoArgsCommand):

    def info(self, message):
        print(" => %s" % message)

    def handle(self, **options):
        call_command('syncdb', interactive=False)
        try:
            User.objects.get(username='admin')
            return
        except User.DoesNotExist:
            pass
        user_args = ('admin', 'lukaszbalcerzak@gmail.com', 'foobar')
        user = User.objects.create_superuser(*user_args)
        self.info("Created user: %s" % user)
        project = Project.objects.create(
            name='frogress',
            url='https://github.com/lukaszb/frogress',
            repo_url='git@github.com:lukaszb/frogress.git',
        )
        self.info("Created project: %s" % project)

        domain = 'localhost:8000'
        site = Site.objects.get_current()
        site.domain = site.name = domain
        site.save()
        self.info("Set current site to %s" % site)

