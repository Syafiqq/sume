# Create your tests here.
from django.test import TestCase

from app.database.seeder import UserSeeder


class UserSeederTest(TestCase):
    def test_generate_user(self):
        self.assertIsNotNone(UserSeeder.seeder)
