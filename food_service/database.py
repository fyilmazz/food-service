from django.db import connection
from django.contrib.auth.models import User


def get_foods():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM FOOD;")
        foods = cursor.fetchall()

    return foods


def get_reviews_with_usernames(username=None):
    with connection.cursor() as cursor:
        if username:
            cursor.execute("SELECT * FROM REVIEWS_WITH_USERNAMES WHERE username = '%s';", username)
        else:
            cursor.execute("SELECT * FROM REVIEWS_WITH_USERNAMES;")
        reviews = cursor.fetchall()

    return reviews


def get_users_with_total_spendings(username=None):
    with connection.cursor() as cursor:
        if username:
            cursor.execute("SELECT * FROM USERS_WITH_TOTAL_SPENDINGS WHERE username = '%s';", username)
        else:
            cursor.execute("SELECT * FROM USERS_WITH_TOTAL_SPENDINGS;")
        users = cursor.fetchall()

    return users


def get_cart_total(username=None):
    with connection.cursor() as cursor:
        if username:
            cursor.execute("SELECT * FROM CALCULATE_CART_TOTAL WHERE username = '%s';", username)
        else:
            cursor.execute("SELECT * FROM CALCULATE_CART_TOTAL;")
        cart_total = cursor.fetchall()

    return cart_total


def get_valid_user_carts():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM VALID_USER_CARTS;")
        user_carts = cursor.fetchall()

    return user_carts


def get_orders_with_usernames(username=None):
    with connection.cursor() as cursor:
        if username:
            cursor.execute("SELECT * FROM ORDERS_WITH_USERNAMES WHERE username = '%s';", username)
        else:
            cursor.execute("SELECT * FROM ORDERS_WITH_USERNAMES;")
        orders = cursor.fetchall()

    return orders


def get_all_orders_of_user(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT f.title, fo.order_date FROM FOOD_ORDER fo"
                       " INNER JOIN CART ca ON ca.cart_id = fo.cart_id"
                       " INNER JOIN CART2FOOD cf ON cf.cart_id = ca.cart_id"
                       " INNER JOIN FOOD f ON f.food_id = cf.food_id"
                       " INNER JOIN CLIENT cl ON cl.client_id = ca.client_id"
                       " WHERE cl.username = '%s' ORDER BY fo.order_date desc;", username)
        orders = cursor.fetchall()

    return orders


def create_user(username, password, address, mail, phone):
    user = User.objects.create_user(username=username, password=password)
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO CLIENT VALUES(client_seq.NEXTVAL, '{0}', '{1}', '{2}', '{3}', '{4}', {5});".format(username, password, address, mail, phone, user.id))
        cursor.execute("INSERT INTO CART (cart_id, client_id) VALUES(cart_seq.NEXTVAL, (SELECT client_id FROM CLIENT WHERE username = '{0}'));".format(username))
        connection.commit()


def add_to_cart(username, title):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO CART2FOOD VALUES(c2f_seq.NEXTVAL, (SELECT cart_id FROM VALID_USER_CARTS WHERE username = '{0}'), (SELECT food_id FROM FOOD WHERE title = '{1}'));"
                       .format(username, title))
        connection.commit()


def create_order(username, payment_type):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO FOOD_ORDER VALUES(food_order_seq.NEXTVAL,"
                       " (SELECT total_price FROM CALCULATE_CART_TOTAL WHERE username = '{0}'),"
                       " SYSDATE, '{1}',"
                       " (SELECT address FROM CLIENT c WHERE username = '{0}'),"
                       " (SELECT cart_id FROM VALID_USER_CARTS WHERE username = '{0}'));".format(username, payment_type))

        cursor.execute("UPDATE CART SET valid = 0 WHERE cart_id = (SELECT cart_id FROM VALID_USER_CARTS WHERE username = '{0}');".format(username))
        cursor.execute("INSERT INTO CART (cart_id, client_id) VALUES(cart_seq.NEXTVAL, (SELECT client_id FROM CLIENT WHERE username = '{0}'));".format(username))
        connection.commit()


def create_review(username, comment, rating):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO REVIEW VALUES(review_seq.NEXTVAL, '{0}', {1}, SYSDATE, (SELECT order_id FROM ORDERS_WITH_USERNAMES WHERE username = '{2}' AND ROWNUM <=1));"
                       .format(comment, rating, username))
        connection.commit()