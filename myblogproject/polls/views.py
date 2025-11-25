from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Choice, Vote

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        messages.error(request, "You didn't select a choice.")
        return redirect('blog:index') # Redirect back to blog index or wherever the poll is shown
    else:
        # Check if user already voted
        if Vote.objects.filter(user=request.user, question=question).exists():
            messages.warning(request, "You have already voted on this poll.")
            return redirect('blog:index')

        selected_choice.votes += 1
        selected_choice.save()
        Vote.objects.create(user=request.user, question=question, choice=selected_choice)
        messages.success(request, "Your vote has been recorded!")
        return redirect('blog:index')

@login_required
def clear_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        # Get the user's vote for this question
        user_vote = Vote.objects.get(user=request.user, question=question)
        
        # Decrease the vote count for the choice
        choice = user_vote.choice
        if choice.votes > 0:
            choice.votes -= 1
            choice.save()
        
        # Delete the vote record
        user_vote.delete()
        
        messages.success(request, "Your vote has been cleared!")
    except Vote.DoesNotExist:
        messages.error(request, "You haven't voted on this poll yet.")
    
    return redirect('blog:index')
