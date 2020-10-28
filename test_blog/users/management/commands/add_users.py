from faker import Faker
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Add dummy users with password 123123123'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

    def handle(self, *args, **options):
        fake = Faker()
        for index in range(options['number']):
            user = User.objects.create_user(
                username=fake.email(),
                email=fake.email(),
                password='123123123')
            user.save()
            if index % 100 == 0 and index != 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully added %s users' % index))

        self.stdout.write(
            self.style.SUCCESS(
                'Script run finished. Successfully added %s users' % options['number']))
