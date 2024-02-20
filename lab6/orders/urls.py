from django.urls import path

from .views import (OrdersView, add_book_to_order, OrderView,
                    remove_book_from_order, delete_order)

urlpatterns = [
    path('<int:user_id>', OrdersView.as_view(), name='orders'),
    path('order/<int:order_id>', OrderView.as_view(), name='order'),
    path('add-book/<int:book_id>', add_book_to_order, name='add-to-order'),
    path('delete/<int:order_id>', delete_order, name='delete-order'),
    path('remove-book/<int:order_id>/<int:book_id>', remove_book_from_order, name='remove-from-order')
]
