from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, CharField, Value
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from itertools import chain
from typing import List, Union

from authentication import forms as auth_forms
from authentication.models import User
from review import forms
from review.models import Ticket, Review, UserFollows


@login_required
def create_ticket(request, ticket_id: Union[int, None] = None):
    """ Create or update a ticket in order to request a review """
    ticket = Ticket.objects.get(id=ticket_id) if ticket_id else None
    ticket_form = forms.TicketForm(request.POST or None,
                                   initial={'ticket_title': ticket.title, 'description': ticket.description,
                                            'image': ticket.image}) if ticket_id else forms.TicketForm()

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)

        if ticket_form.is_valid():

            if not ticket:
                # Create the ticket
                ticket = Ticket(user_id=request.user.id)
                ticket.time_created = timezone.now()
            ticket.title = ticket_form.cleaned_data['ticket_title']
            ticket.description = ticket_form.cleaned_data['description']
            if request.FILES and request.FILES['image']:
                ticket.image = ticket_form.cleaned_data['image']

            try:
                ticket.save()
            except Exception as e:
                messages.error(request, e)
            else:
                messages.success(request, 'Ticket was successfully inserted !')

    return render(request, 'review/create_ticket.html', locals())


@login_required
def create_review(request):
    """ Create a review """
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    tickets = Ticket.objects.all()

    if request.method == 'POST':

        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if ticket_form.is_valid():

            ticket = Ticket(user_id=request.user.id)
            ticket.title = ticket_form.cleaned_data['ticket_title']
            ticket.description = ticket_form.cleaned_data['description']
            if request.FILES and request.FILES['image']:
                ticket.image = ticket_form.cleaned_data['image']
            ticket.time_created = timezone.now()
            ticket.save()

            if review_form.is_valid():

                # Ticket has been created, so create the related review
                review = Review(ticket=ticket)
                review.rating = review_form.cleaned_data['rating']
                review.headline = review_form.cleaned_data['review_title']
                review.body = review_form.cleaned_data['comment']
                review.user_id = request.user.id
                review.time_created = timezone.now()
                try:
                    review.save()
                except Exception as e:
                    messages.error(request, e)
                else:
                    ticket.replied = True
                    ticket.save()
                    messages.success(request, 'Ticket and related review has successfully added !')

    return render(request, 'review/create_review.html', locals())


@login_required
def flow(request):
    """ Display the last tickets and their related review ordered by time created """
    followed_users = [u.followed_user_id for u in UserFollows.objects.filter(user=request.user)] + [request.user.id]
    tickets = Ticket.objects.filter(user_id__in=followed_users).order_by('-time_created') if followed_users else None
    flow: List[dict] = []
    for ticket in tickets:
        if ticket.replied:
            review = Review.objects.get(ticket=ticket)
            flow += [{'ticket_id': ticket.id, 'title': ticket.title, 'description': ticket.description,
                      'user': ticket.user, 'image': ticket.image, 'time_created': ticket.time_created,
                      'replied': ticket.replied, 'rating': review.rating * '★' + (5 - review.rating) * '☆',
                      'headline': review.headline, 'body': review.body, 'review_user': review.user,
                      'review_time_created': review.time_created}]
        else:
            flow += [{'ticket_id': ticket.id, 'title': ticket.title, 'description': ticket.description,
                      'user': ticket.user, 'image': ticket.image, 'time_created': ticket.time_created,
                      'replied': ticket.replied}]

    return render(request, 'review/flow.html', locals())


@login_required
def my_posts(request):
    """ Display all the reviews and tickets of the current user """
    tickets = Ticket.objects.filter(user_id=request.user.id).annotate(content_type=Value('ticket', CharField()))
    reviews = Review.objects.filter(user_id=request.user.id).annotate(content_type=Value('review', CharField()))
    posts = sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)

    return render(request, 'review/posts.html', locals())


@login_required
def delete_element(request, review_id: Union[int, None] = None, ticket_id: Union[int, None] = None):
    """ Delete a ticket or a review """
    if review_id:
        review = Review.objects.get(id=review_id)
        if review.user != request.user:
            messages.warning(request, 'Vous ne pouvez pas supprimer cette critique, '
                                      'car vous en êtes pas le propriétaire !')
        else:
            try:
                review.delete()
            except Exception as e:
                messages.warning(request, f'Erreur survenue lors de la suppression de la critique: {e}')
            else:
                review.ticket.replied = False
                review.ticket.save()
                messages.success(request, 'Cet article a bien été supprimé !')
    elif ticket_id:
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.user != request.user:
            messages.warning(request, 'Vous ne pouvez pas supprimer ce ticket, car vous en êtes pas le propriétaire !')
        else:
            try:
                ticket.delete()
            except Exception as e:
                messages.warning(request, f'Erreur survenue lors de la suppression du ticket: {e}')
            else:
                messages.success(request, 'Ce ticket a bien été supprimé !')
    else:
        messages.warning(request, 'Le système ne comprend pas votre demande...')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def review_from_ticket(request, ticket_id: int, review_id: Union[int, None] = None):
    """ Create or update a review from a specific ticket """
    ticket = Ticket.objects.get(id=ticket_id)
    review = Review.objects.get(id=review_id) if review_id else None
    review_form = forms.ReviewForm(
        request.POST or None, initial={'rating': review.rating, 'review_title': review.headline,
                                       'comment': review.body}, label_suffix='') if review_id else forms.ReviewForm()

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)

        if review_form.is_valid():

            if not review:
                # Create the review
                review = Review(ticket=ticket)
                review.user_id = request.user.id
                review.time_created = timezone.now()
            review.rating = review_form.cleaned_data['rating']
            review.headline = review_form.cleaned_data['review_title']
            review.body = review_form.cleaned_data['comment']

            try:
                review.save()
            except Exception as e:
                messages.error(request, e)
            else:
                ticket.replied = True
                ticket.save()
                messages.success(request, 'review was successfully saved !')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'review/review_from_ticket.html', locals())


@login_required
def subscription(request):
    """ Subscribe management """
    followed_users: UserFollows = UserFollows.objects.filter(user=request.user)
    subscribers: UserFollows = UserFollows.objects.filter(followed_user_id=request.user.id)

    username_form = auth_forms.UsernameForm()
    if request.method == 'POST':
        username_form = auth_forms.UsernameForm(request.POST)
        if username_form.is_valid():
            searched_person = username_form.cleaned_data['username']
            returned_users = User.objects.filter(username__icontains=searched_person)

    return render(request, 'review/subscription.html', locals())


@login_required
def follow_a_user(request, user_id: int):
    """ Subscribe to a user """
    already_exists = UserFollows.objects.filter(Q(user_id=request.user.id) & Q(followed_user_id=user_id))
    if not already_exists:
        followed_user: UserFollows = UserFollows()
        followed_user.user_id = request.user.id
        followed_user.followed_user_id = user_id
        followed_user.save()
        messages.success(request, 'Vous êtes maintenant abonné à cet utilisateur')
    else:
        messages.warning(request, 'Vous êtes déjà abonné à cet utilisateur !')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow_a_user(request, user_id: int):
    """ Unfollow a user """
    try:
        user_follow = UserFollows.objects.get(Q(user_id=request.user.id) & Q(followed_user_id=user_id))
    except ObjectDoesNotExist as e:
        messages.error(request, f'La demande de désabonnement a échoué: {e}')
    else:
        try:
            user_follow.delete()  # Check model delete to know the errors to manage
        except Exception as e:
            messages.error(request, f'La demande de désabonnement a échoué: {e}')
        else:
            messages.success(request, 'Vous vous êtes désabonné avec succès !')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
