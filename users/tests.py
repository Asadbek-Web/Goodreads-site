from urllib import response
from users.models import CustomUser
from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse



class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "asadbek",
                "first_name": "Asadbek",
                "last_name": "Abdumalikov",
                "email": "asadbekabdumalikovfifth@gmail.com",
                "password": "smth"
            }
        )

        user = CustomUser.objects.get(username="asadbek")

        self.assertEqual(user.first_name, "Asadbek")
        self.assertEqual(user.last_name, "Abdumalikov")
        self.assertEqual(user.email, "asadbekabdumalikovfifth@gmail.com")
        self.assertNotEqual(user.password, "smth")


    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "asadbek",
                "email": "asadbekabdumalikovfifith@gmail.com",
            }
        )


        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")


    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={

                "username": "asadbek",
                "first_name": "Asadbek",
                "last_name": "Abdumalikov",
                "email": "invalid-email",
                "password": "smth"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")


    def test_unique_username(self):
        user = CustomUser.objects.create(username="asadbek", first_name="Asadbek")
        user.set_password("somepassword")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "asadbek",
                "first_name": "Asadbek",
                "last_name": "Abdumalikov",
                "email": "asadbekabdumalikovfifth@gmail.com",
                "password": "smth"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")



class LoginTestCase(TestCase):
    # DRY --> Don't repeat yourself
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="asadbek", first_name="Asadbek")
        self.db_user.set_password("somepassword")
        self.db_user.save()
    
    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data = {
                'username':'asadbek',
                'password':'somepassword',
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                'username': 'wrong-username',
                'password': 'somepassword',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


        self.client.post(
            reverse("users:login"),
            data={
                'username': 'asadbek',
                'password': 'wrong-password',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


    def test_logout(self):
        self.client.login(username="asadbek", password="somepassword")
        
        self.client.get(reverse("users:logout"))
        
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        
        
        

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))
        
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/") 
        
    
    
    def test_profile_details(self):
        user = CustomUser.objects.create( 
            username="asadbek", first_name="Asadbek", last_name="Abdumalikov", email="asadbekabdumalikovfifth@gmail.com"
        )
        
        user.set_password("somepassword")
        user.save()
        
        self.client.login(username="asadbek", password="somepassword")
        
        response = self.client.get(reverse("users:profile"))
        
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
        

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="asadbek",  first_name="Asadbek", last_name="Abdumalikov", email="asadbekabdumalikovfifth@gmail.com"
        )
        
        user.set_password("somepassword")
        user.save()
        self.client.login(username="asadbek", password="somepassword")
        
        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "asadbek",
                "first_name": "Asadbek",
                "last_name": "Tommy",
                "email": "asadbek123@gmail.com"
            }
        )

        user.refresh_from_db()
        # user = User.objects.get(pk=user.pk)

        self.assertEqual(user.last_name, "Tommy")
        self.assertEqual(user.email, "asadbek123@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))