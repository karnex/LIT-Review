from django.urls import path

from review import views

urlpatterns = [
    path('create-a-review', views.create_review, name='create_review'),
    path('delete-review-<review_id>', views.delete_element, name='delete_review'),
    path('delete-ticket-<ticket_id>', views.delete_element, name='delete_ticket'),
    path('review-from-ticket-<ticket_id>', views.review_from_ticket, name='review_from_ticket'),
    path('review-<review_id>-from-ticket-<ticket_id>', views.review_from_ticket, name='review_from_ticket'),
    path('create-a-ticket', views.create_ticket, name='create_ticket'),
    path('update-a-ticket-<ticket_id>', views.create_ticket, name='update_ticket'),
    path('flow', views.flow, name='flow'),
    path('posts', views.my_posts, name='posts'),
    path('subscription', views.subscription, name='subscription'),
    path('follow-user-<user_id>', views.follow_a_user, name='follow_a_user'),
    path('unfollow-user-<user_id>', views.unfollow_a_user, name='unfollow_a_user'),
]
