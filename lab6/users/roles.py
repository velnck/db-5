from django.db import connection


def get_admin_role_id():
    with connection.cursor() as cursor:
        return cursor.execute("SELECT id FROM roles "
                              "WHERE name = 'Администратор'").fetchone()[0]


def get_employee_role_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM roles "
                       "WHERE name = 'Работник'")
        return cursor.fetchone()[0]


def get_customer_role_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM roles "
                       "WHERE name = 'Пользователь'")
        return cursor.fetchone()[0]
