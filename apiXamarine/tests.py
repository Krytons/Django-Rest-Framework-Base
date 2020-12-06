from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
class UserAccountTest(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser('test@super.com', 'name', 'surname', 'nickname', 'password')
        self.assertEqual(super_user.email, 'test@super.com')
        self.assertEqual(super_user.nickname, 'nickname')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "Nickname: nickname")

        with self.assertRaises(ValueError):
            db.objects.create_superuser(email='test2@super.com', name='admintest', surname='admintest',
                                        nickname='admintest', password='testtest', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(email='test2@super.com', name='admintest', surname='admintest',
                                        nickname='admintest', password='testtest', is_staff=False)


    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user('test@user.com', 'name', 'surname', 'nickname', 'password')
        self.assertEqual(user.email, 'test@user.com')
        self.assertEqual(user.nickname, 'nickname')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(email='', name='test', surname='test',
                                        nickname='test', password='testtest')





