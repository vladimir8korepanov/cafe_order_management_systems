from django.urls import path
from .views import (
    order_list,  # Список заказов
    order_create, # Создание нового заказа
    order_edit, # Редактирование заказа
    order_delete, # Удаление заказа 
    revenue_view, # Страница выручки
    order_detail # Детали заказа
    
)

urlpatterns = [
    path('', order_list, name='order_list'), # Главная страница 
    path('create/', order_create, name='order_create'), # Создание нового заказа
    path('<int:order_id>/edit/', order_edit, name='order_edit'), # Редактирование заказа по ID 
    path('<int:order_id>/delete/', order_delete, name='order_delete'), # Удаление 
    path('revenue/', revenue_view, name='revenue'), #Страница выручка
    path('detail/<int:order_id>/', order_detail, name='order_detail'), # Детали заказа
]
