from django.core.management.base import NoArgsCommand, CommandError
from proj.gather.views import generate_and_store_map_data

class Command(NoArgsCommand):
    help = 'Generates STATIC_ROOT/map_data.json'

    def handle_noargs(self, **options):
        generate_and_store_map_data()
