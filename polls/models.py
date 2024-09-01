import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """
    Represents a question in the poll.

    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The date when the question was published.
        end_date (datetime): The date when the question ends (optional).
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date ended', null=True, blank=True)

    def __str__(self):
        """
        Return the text of the question.

        Returns:
            str: The text of the question.
        """
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """
        Determine if the question was published recently.

        Returns:
            bool: True if the question was published within the last day, otherwise False.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Is published?',
    )
    def is_published(self):
        """
        Determine if the question is published.

        Returns:
            bool: True if the current time is on or after the publication date, otherwise False.
        """
        now = timezone.localtime()
        return now >= self.pub_date

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Can vote?',
    )
    def can_vote(self):
        """
        Determine if the question is open for voting.

        Returns:
            bool: True if the current time is between the publication date and end date, otherwise False.
        """
        now = timezone.localtime()
        if self.end_date:
            return self.pub_date <= now <= self.end_date
        return now >= self.pub_date


class Choice(models.Model):
    """
    Represents a choice for a question in the poll.

    Attributes:
        question (Question): The question to which the choice belongs.
        choice_text (str): The text of the choice.
        votes (int): The number of votes for this choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Return the text of the choice.

        Returns:
            str: The text of the choice.
        """
        return self.choice_text
