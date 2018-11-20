from django.db import connection
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('django')


def get_foods():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM FOOD;")
        foods = cursor.fetchall()

    return foods


def get_reviews_with_usernames(username=None):
    with connection.cursor() as cursor:
        if username:
            cursor.execute("SELECT * FROM REVIEWS_WITH_USERNAMES WHERE username = '{0}';".format(username))
        else:
            cursor.execute("SELECT * FROM REVIEWS_WITH_USERNAMES;")
        reviews = cursor.fetchall()

    return reviews


def get_users_with_total_spendings(username=None):
    with connection.cursor() as cursor:
        if username:
            cursor.execute("SELECT total_spending FROM USERS_WITH_TOTAL_SPENDINGS WHERE username = '{0}';".format(username))
            total_spend = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM USERS_WITH_TOTAL_SPENDINGS;")
            total_spend = cursor.fetchall()

    return total_spend


def get_cart_total(username=None):
    with connection.cursor() as cursor:
        if username:
            cursor.execute("SELECT total_price FROM CALCULATE_CART_TOTAL WHERE username = '{0}';".format(username))
            cart_total = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM CALCULATE_CART_TOTAL;")
            cart_total = cursor.fetchall()

    return cart_total


def get_foods_in_cart(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT f.title, f.price FROM FOOD f"
                       " INNER JOIN CART2FOOD cf ON cf.food_id=f.food_id"
                       " INNER JOIN CART ca ON ca.cart_id = cf.cart_id"
                       " INNER JOIN CLIENT cl ON cl.client_id = ca.client_id"
                       " WHERE ca.valid = 1 AND cl.username = '{0}';".format(username))
        cart_foods = cursor.fetchall()
    return cart_foods


def get_valid_user_carts():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM VALID_USER_CARTS;")
        user_carts = cursor.fetchall()

    return user_carts


def get_orders_with_usernames(username=None):
    with connection.cursor() as cursor:
        if username:
            cursor.execute("SELECT * FROM ORDERS_WITH_USERNAMES WHERE username = '{0}';".format(username))
        else:
            cursor.execute("SELECT * FROM ORDERS_WITH_USERNAMES;")
        orders = cursor.fetchall()

    return orders


def get_all_orders_of_user(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT fo.order_id, fo.total_price, TO_CHAR(fo.order_date, 'DD.MM.YYYY'), f.title, re.review_comment, re.rating FROM FOOD_ORDER fo"
                       " INNER JOIN CART ca ON ca.cart_id = fo.cart_id"
                       " INNER JOIN CART2FOOD cf ON cf.cart_id = ca.cart_id"
                       " INNER JOIN FOOD f ON f.food_id = cf.food_id"
                       " INNER JOIN CLIENT cl ON cl.client_id = ca.client_id"
                       " LEFT JOIN REVIEW re ON re.order_id = fo.order_id"
                       " WHERE cl.username = '{0}' ORDER BY fo.order_date desc;".format(username))
        orders = cursor.fetchall()

    return orders


def create_user(user_id, username, address, phone):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO CLIENT VALUES(client_seq.NEXTVAL, '{0}', '{1}', '{2}', {3});".format(username, address, phone, user_id))
        cursor.execute("INSERT INTO CART (cart_id, client_id) VALUES(cart_seq.NEXTVAL, (SELECT client_id FROM CLIENT WHERE username = '{0}'));".format(username))
        connection.commit()


def add_to_cart(username, food_id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO CART2FOOD VALUES(c2f_seq.NEXTVAL, (SELECT cart_id FROM VALID_USER_CARTS WHERE username = '{0}'), {1});"
                       .format(username, food_id))
        connection.commit()


def give_order(username, payment_type):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO FOOD_ORDER VALUES(food_order_seq.NEXTVAL,"
                           " (SELECT total_price FROM CALCULATE_CART_TOTAL WHERE username = '{0}'),"
                           " SYSDATE, '{1}',"
                           " (SELECT address FROM CLIENT c WHERE username = '{0}'),"
                           " (SELECT cart_id FROM VALID_USER_CARTS WHERE username = '{0}'));".format(username, payment_type))

            cursor.execute("UPDATE CART SET valid = 0 WHERE cart_id = (SELECT cart_id FROM VALID_USER_CARTS WHERE username = '{0}');".format(username))
            cursor.execute("INSERT INTO CART (cart_id, client_id) VALUES(cart_seq.NEXTVAL, (SELECT client_id FROM CLIENT WHERE username = '{0}'));".format(username))
            connection.commit()
    except Exception as e:
        logger.exception(e)


def add_review(order_id, comment, rating):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO REVIEW VALUES(review_seq.NEXTVAL, '{0}', {1}, SYSDATE, {2});"
                       .format(comment, rating, order_id))
        connection.commit()


def reset_cart(username):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM CART2FOOD WHERE cart_id = (SELECT cart_id FROM VALID_USER_CARTS WHERE username = '{0}');"
                       .format(username))
        connection.commit()


def add_trigger():
    with connection.cursor() as cursor:
        cursor.execute("CREATE OR REPLACE TRIGGER  FOOD_TYPE_ID_TRIGGER"
                       " before insert on FOOD_TYPE"
                       " for each row"
                       " begin"
                       " if :NEW.TYPE_ID is null then"
                       " :NEW.TYPE_ID := food_type_seq.nextval;"
                       " end if;"
                       " end; ")
        connection.commit()