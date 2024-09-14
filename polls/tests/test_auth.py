"""Tests of authentication."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from mysite import settings

from polls.models import Question, Choice


class AuthenticationTests(TestCase):
    def setUp(self):
        """
        Set up initial data for testing.
        """
        super().setUp()
        self.password = "test1234"
        self.tester = User.objects.create_user(username="tester",
                                               password=self.password)
        self.tester.first_name = "Tester"
        self.tester.save()
        self.question = Question.objects.create(question_text="Test question")
        self.question.save()
        for n in range(1, 4):
            self.choice = Choice(choice_text=f"Test choice {n}",
                                 question=self.question)
            self.choice.save()

    def test_login(self):
        """
        If the visitor log in with the correct username and password,
        they will move to the index page.
        """
        login = reverse("login")
        response = self.client.get(login)
        self.assertEqual(200, response.status_code)

        response = self.client.post(login, {"username": self.tester.username,
                                            "password": self.password})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_signup(self):
        """
        If the visitor register with a valid username and password,
        they will move to the index page.
        """
        signup = reverse("signup")
        response = self.client.post(signup, {"username": "Tester_Signup",
                                             "password1": "TS12345678",
                                             "password2": "TS12345678"})
        self.assertTrue(User.objects.filter(username="Tester_Signup").exists())
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("polls:index"))

    def test_logout(self):
        """
        Test user logout.
        After the user logs out, they will move to the login page.
        """
        logout = reverse("logout")
        self.assertTrue(self.client.login(username=self.tester.username,
                                          password=self.password))
        response = self.client.get(logout)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_auth_required_to_vote(self):
        """Authentication is required to submit a vote.

        As an unauthenticated user,
        when I submit a vote for a question,
        then I am redirected to the login page
        or I receive a 403 response (FORBIDDEN)
        """
        vote = reverse('polls:vote', args=[self.question.id])
        choice = self.question.choice_set.first()
        form_data = {"choice": f"{choice.id}"}
        response = self.client.post(vote, form_data)
        self.assertEqual(302, response.status_code)
        login_with_next = f"{reverse('login')}?next={vote}"
        self.assertRedirects(response, login_with_next)