import mysql.connector
import os
import time

def get_connection():
    while True:
        try:
            return mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DB")
            )
        except Exception as e:
            print(f"[MySQL] retry... {e}")
            time.sleep(3)


def insert_order(user_id, product_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO orders (user_id, product_id, quantity, status)
    VALUES (%s, %s, %s, 'PENDING')
    """
    cursor.execute(query, (user_id, product_id, quantity))
    conn.commit()

    order_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return order_id
