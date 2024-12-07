from django.test import TestCase
from django.contrib.auth import get_user_model


class TestCustomUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser', email='test@mail.com', password='1234')

    def test_customuser_model(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@mail.com')
        self.assertEquals(self.user.check_password("1234"), True)