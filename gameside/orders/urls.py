from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<int:order_pk>/', views.order_detail, name='order-datail'),
    path('<int:order_pk>/games/', views.order_game_list, name='order-game-list'),
    path('<int:order_pk>/games/add/', views.add_game_to_order, name='add-game-to-order'),
]
