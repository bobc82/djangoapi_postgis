from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Print number to be printed')
        #optional argument
        parser.add_argument('-p', '--prefix', type=str, help='Define a prefix', )

    def handle(self, *args, **kwargs):
        #time = timezone.now().strftime('%X')
        #self.stdout.write("It's now %s" % time)
        total = kwargs['total']
        prefix = kwargs['prefix']
        print(total)
        if prefix:
            print(prefix)