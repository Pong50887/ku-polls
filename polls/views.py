"""
Views for handling poll-related functionality in the Polls application.
"""

from logging import getLogger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """
    Display the list of the latest five published poll questions.

    Attributes:
        template_name (str): The template for rendering the view.
        context_object_name (str): The name of the context variable containing the list of questions.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


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
    """Return the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """
    vote() is responsible for handling user votes on a poll question.
    """
    question = get_object_or_404(Question, pk=question_id)
    requested_user = request.user
    ip_address = get_client_ip(request)
    logger = getLogger('polls')
    logger.info(f'{requested_user} logged in from {ip_address}')

    if not question.can_vote():
        messages.error(request, message=f"Poll {question_id} is not available "
                                        f"for voting.")
        return redirect('polls:index')
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        logger.warning(f'{requested_user} failed to vote {question} from '
                       f'{ip_address}')
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    try:
        # Find a vote for this user and this question
        selected_vote = Vote.objects.get(user=requested_user,
                                         choice__question=question)
        # Update his vote
        selected_vote.choice = selected_choice
    except Vote.DoesNotExist:
        # No matching vote - Create a new Vote
        selected_vote = Vote(user=requested_user, choice=selected_choice)
    selected_vote.save()
    logger.info(f'{requested_user} voted for {selected_choice} '
                f'in {question} from {ip_address}')
    messages.info(request, message=f"You voted for \"{selected_choice}\".")
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,
                                                               )))
