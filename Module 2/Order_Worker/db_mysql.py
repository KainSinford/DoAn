import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="orders"
    )

def update_order_status(order_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE orders SET status=%s WHERE id=%s"
    cursor.execute(query, (status, order_id))
    conn.commit()

    cursor.close()
    conn.close()