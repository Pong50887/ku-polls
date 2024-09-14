from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from mysite import settings
from polls.models import Question, Choice


class AuthenticationTest(TestCase):
    def setUp(self):
        """
        Set up essential components to be used in authentication tests.
        Create a test user, a test question, and choices.
        """
        super().setUp()
        self.username = 'tester'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.user.save()
        self.question = Question.objects.create(question_text='Test Question')
        for count in range(1, 5):
            choice = Choice(choice_text=f'Choice {count}',
                            question=self.question)
            choice.save()
        self.question.save()

    def test_login_page(self):
        """
        Login page testing for both GET and POST methods.
        GET request should return a 200 OK response.
        POST request should return a 302 redirect to the polls index page.
        """
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        form_data = {'username': self.username, 'password': self.password}
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_auth_required_to_vote(self):
        """
        Test for voting without log in to redirect to log in page.
        Unauthenticated user will be redirected to log in page.
        """
        vote_url = reverse('polls:vote', args=[self.question.id])
        choice = self.question.choice_set.first()
        form_data = {'choice': f'{choice.id}'}
        response = self.client.post(vote_url, form_data)
        self.assertEqual(302, response.status_code)
        login_next_url = f"{reverse('login')}?next={vote_url}"
        self.assertRedirects(response, login_next_url)

    def test_signup_page(self):
        """
        Signup page testing for both GET and POST methods.
        GET request should return a 200 OK response.
        POST request should return a 302 redirect to the polls index page.
        """
        signup_url = reverse("signup")
        response = self.client.get(signup_url)
        self.assertEqual(200, response.status_code)
        form_data = {'username': 'new_tester', 'password1': self.password,
                     'password2': self.password}
        response = self.client.post(signup_url, form_data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('polls:index'))

    def test_login_with_unsigned_up_user(self):
        """
        An unsigned up user cannot log in.
        The login page should show the message
        "Please enter a correct username and password."
        and not redirect to other page.
        """
        login_url = reverse("login")
        form_data = {'username': 'new_user', 'password': self.password}
        response = self.client.post(login_url, form_data)
        self.assertEqual(200, response.status_code)
        self.assertContains(response,
                            'Please enter a correct username and password.')

    def test_login_with_incorrect_password(self):
        """
        When a user try to log in with an incorrect password, the login page
        should show the message
        "Please enter a correct username and password."
        and not redirect to other page.
        """
        login_url = reverse("login")
        form_data = {'username': self.username, 'password': 'wrongpassword123'}
        response = self.client.post(login_url, form_data)
        self.assertEqual(200, response.status_code)
        self.assertContains(response,
                            'Please enter a correct username and password.')