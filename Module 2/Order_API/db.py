import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="orders"
    )

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
