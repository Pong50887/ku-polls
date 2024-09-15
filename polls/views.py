"""Views for handling poll-related functionality in the Polls application."""
from logging import getLogger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import logging

class IndexView(generic.ListView):
    """
    Display the list of all published poll questions.

    Attributes:
        template_name (str): The template for rendering the view.
        context_object_name (str): The name of the context variable containing the list of questions.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return published questions."""
        published_question_list = [q.pk for q in Question.objects.all()
                                   if q.is_published()]
        published_questions = (Question.objects.filter
                               (pk__in=published_question_list))
        return published_questions.order_by('-pub_date')


class DetailView(generic.DetailView):
    """
    Display the details of a poll question.

    Attributes:
        model (Question): The model representing the poll question.
        template_name (str): The template for rendering the view.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handles the HTTP GET request for the poll detail page.
        It will be redirected to the poll index page only if
        the poll question does not exist or voting is not allowed.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except (Question.DoesNotExist, Http404):
            messages.error(request, f"Poll question {kwargs['pk']}"
                                    f" does not exist.")
            return redirect("polls:index")

        this_user = request.user
        try:
            prev_vote = Vote.objects.get(user=this_user,
                                         choice__question=question)
        except (Vote.DoesNotExist, TypeError):
            prev_vote = None

        if not question.can_vote():
            messages.error(request, f"Poll question {kwargs['pk']}"
                                    f" does not allow voting.")
            return redirect("polls:index")
        else:
            return render(request, self.template_name,
                          {"question": question,
                           "prev_vote": prev_vote})


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


logger = logging.getLogger('polls')


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Handle voting for a specific question."""
    question = get_object_or_404(Question, pk=question_id)
    this_user = request.user
    ip_address = get_client_ip(request)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        logger.warning(f"{this_user} failed to vote in {question} "
                       f"from {ip_address}")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    try:
        user_vote = Vote.objects.get(user=this_user, choice__question=question)
        user_vote.choice = selected_choice
        user_vote.save()
        logger.info(f'{this_user} voted for Choice {selected_choice.id} '
                    f'in Question {question.id} from {ip_address}')
        messages.success(request, f"Your vote was updated to "
                                  f"'{selected_choice.choice_text}'")
    except Vote.DoesNotExist:
        Vote.objects.create(user=this_user, choice=selected_choice)
        logger.info(f'{this_user} voted for Choice {selected_choice.id} '
                    f'in Question {question.id} from {ip_address}')
        messages.success(request, f"You voted for "
                                  f"'{selected_choice.choice_text}'")

    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


@receiver(user_logged_in)
def log_user_login(request, user, **kwargs):
    """Log a message when a user successfully logs in."""
    ip_address = get_client_ip(request)
    logger.info(f'{user} logged in from {ip_address}')


@receiver(user_logged_out)
def log_user_logout(request, user, **kwargs):
    """Log a message when a user successfully logs out."""
    ip_address = get_client_ip(request)
    logger.info(f'{user} logged out from {ip_address}')


@receiver(user_login_failed)
def log_user_login_failed(request, **kwargs):
    """Log a message when a user login attempt fails."""
    ip_address = get_client_ip(request)
    logger.warning(f'User failed to log in from {ip_address}')
