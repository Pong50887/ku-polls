import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelVoteTests(TestCase):
    def test_can_vote_after_pub_date_before_end_date(self):
        """
        can_vote() returns True if the pub_data is in the past
        and end_date is in the future.
        """
        past = timezone.now() - datetime.timedelta(days=30)
        future = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date=past, end_date=future)
        self.assertTrue(question.can_vote())

    def test_can_vote_after_pub_date_null_end_date(self):
        """
        can_vote() returns True if the pub_data is in the past
        and end_date is null.
        """
        past = timezone.now() - datetime.timedelta(days=30)
        question = Question(pub_date=past)
        self.assertTrue(question.can_vote())

    def test_cannot_vote_before_pub_date(self):
        """
        can_vote() returns False if the pub_date is in the future.
        """
        future = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date=future)
        self.assertFalse(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        can_vote() returns False if the end_date is in the past.
        """
        past = timezone.now() - datetime.timedelta(days=30)
        question = Question(end_date=past)
        self.assertFalse(question.can_vote())
