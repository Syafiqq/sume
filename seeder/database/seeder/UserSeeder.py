from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django_seed import Seed


def seed():
    seeder = Seed.seeder()

    seeder.add_entity(User, 1, {
        'username': lambda x: 'root',
        'email': lambda x: 'root@mail.com',
        'password': lambda x: make_password('secret'),
        'is_superuser': lambda x: True
    })
    seeder.add_entity(User, 5, {
        'username': lambda x: seeder.faker.name(),
        'email': lambda x: seeder.faker.safe_email(),
        'password': lambda x: make_password('secret'),
        'is_superuser': lambda x: False
    })
    seeder.execute()
