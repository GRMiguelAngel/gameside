from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game-list'),
    path('<str:game_slug>/', views.game_detail, name='game-detail'),
    path('<str:game_slug>/', views.game_detail, name='game-detail'),
    path('reviews/<int:review_pk>/', views.review_detail, name='review-detail'),
    path('<str:game_slug>/reviews/', views.game_reviews, name='game-reviews'),
    path('<str:game_slug>/reviews/add/', views.add_review, name='add-review'),
]
