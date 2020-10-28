from datetime import timezone
from faker import Faker
from random import randint
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from test_blog.blog.models import Post

User = get_user_model()


class Command(BaseCommand):
    help = 'Add dummy posts for existing users'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int)

        parser.add_argument(
            '--user',
            help='Add products for specific user',
        )

    def handle(self, *args, **options):
        fake = Faker()
        user = None
        if (options['user']):
            try:
                user = User.objects.get(id=options['user'])
            except User.DoesNotExist:
                raise CommandError(
                    'User "%s" does not exist' % options['user'])
        if user is None:
            user_ids = User.objects.all().values_list(
                'id', flat=True).distinct()
        for index in range(options['number']):
            if user is None:
                current_user = User.objects.get(
                    id=user_ids[randint(0, len(user_ids) - 1)])
            else:
                current_user = user
            post = Post(
                header='Fake {}'.format(fake.text(max_nb_chars=56)),
                text='Fake {}'.format(fake.text(max_nb_chars=255)),
                user=current_user
            )
            post.save()
            post.created = fake.date_time_between(
                    start_date='-1y', end_date='now',
                    tzinfo=timezone.utc)
            post.save()
            if index % 100 == 0 and index != 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully added %s posts' % index))

        self.stdout.write(
            self.style.SUCCESS(
                'Script run finished. Successfully added %s posts' % options['number']))
