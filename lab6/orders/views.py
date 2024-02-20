from django.db import connection, DatabaseError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from orders.models import Orders


class OrdersView(View):
    template_name = 'orders/all.html'

    def get(self, request, user_id):
        if not request.user.is_staff:
            return HttpResponse('Unauthorized', 401)
        if user_id == 0:
            orders = Orders.objects.raw(
                "SELECT users.username AS username, "
                "orders.id AS id, orders.user_id, orders.sum_total, "
                "ARRAY_TO_JSON(ARRAY_AGG(JSON_BUILD_OBJECT("
                "'book_title', books.title, "
                "'book_id', books.id, "
                "'qt', orders_books.quantity))) "
                "AS items, orders.delivery_address "
                "FROM orders LEFT JOIN orders_books "
                "ON orders.id = orders_books.order_id "
                "LEFT JOIN books ON books.id = orders_books.book_id "
                "JOIN users ON orders.user_id = users.id "
                "GROUP BY orders.id, orders.user_id, "
                "users.username"
            )
        else:
            orders = Orders.objects.raw(
                "SELECT users.username AS username, "
                "orders.id AS id, orders.user_id, orders.sum_total, "
                "ARRAY_TO_JSON(ARRAY_AGG(JSON_BUILD_OBJECT("
                "'book_title', books.title, "
                "'book_id', books.id, "
                "'qt', orders_books.quantity))) "
                "AS items, orders.delivery_address "
                "FROM orders LEFT JOIN orders_books "
                "ON orders.id = orders_books.order_id "
                "LEFT JOIN books ON books.id = orders_books.book_id "
                "JOIN users ON orders.user_id = users.id "
                "WHERE user_id = %s GROUP BY orders.id, "
                "orders.user_id, users.username",
                [user_id])
        return render(request, self.template_name, {
            'orders': orders,
        })


def add_book_to_order(request, book_id):
    orders = Orders.objects.raw(
        "SELECT * FROM orders WHERE "
        "user_id = %s "
        "AND NOT is_commited",
        [request.user.id])
    # get order_id if exist
    # if not then create new
    if len(orders) > 0:
        order_id = orders[0].id
    else:
        order_id = (
            connection.cursor().execute(
                "INSERT INTO orders (user_id, is_commited)"
                "VALUES (%s, False) RETURNING id",
                [request.user.id])).fetchone()
    try:
        connection.cursor().execute("CALL add_book_to_order(%s, %s)",
                                    [order_id, book_id])
    except DatabaseError as e:
        return HttpResponse('Нет в наличии')
    return redirect('order', order_id=order_id)


class OrderView(View):
    template_name = 'orders/order.html'

    def get(self, request, order_id):
        order = Orders.objects.raw(
            "SELECT orders.id AS id, orders.sum_total, "
            "ARRAY_TO_JSON(ARRAY_AGG(JSON_BUILD_OBJECT("
            "'book_title', books.title, "
            "'book_id', books.id, "
            "'qt', orders_books.quantity))) "
            "AS items, orders.delivery_address "
            "FROM orders LEFT JOIN orders_books "
            "ON orders.id = orders_books.order_id "
            "LEFT JOIN books ON books.id = orders_books.book_id "
            "JOIN users ON orders.user_id = users.id "
            "WHERE orders.id = %s GROUP BY orders.id",
            [order_id])
        return render(request, self.template_name,
                      context={
                          'order': order[0],
                      })

    def post(self, request, order_id):
        connection.cursor().execute(
            "UPDATE orders SET delivery_address = %s WHERE id = %s",
            [request.POST['address'], order_id]
        )
        try:
            connection.cursor().execute(
                "CALL commit_order(%s)",
                [order_id])
        except DatabaseError as e:
            return HttpResponse(e)
        return redirect('orders', user_id=request.user.id)


def remove_book_from_order(request, order_id, book_id):
    connection.cursor().execute(
        "CALL remove_book_from_order(%s, %s)",
        [order_id, book_id])
    return redirect('order', order_id=order_id)


def delete_order(request, order_id):
    if request.user.is_staff:
        try:
            connection.cursor().execute(
                "CALL delete_order(%s)",
                [order_id])
        except DatabaseError as e:
            return HttpResponse(e)
        return redirect('main')
    else:
        return HttpResponse('Unauthorized', 401)
