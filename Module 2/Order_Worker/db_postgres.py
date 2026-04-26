import psycopg2

def get_connection():
    return psycopg2.connect(
        host="postgres",
        database="finance",
        user="postgres",
        password="postgres"
    )

def insert_transaction(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO transactions (order_id, user_id, product_id, quantity)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        data["order_id"],
        data["user_id"],
        data["product_id"],
        data["quantity"]
    ))

    conn.commit()
    cursor.close()
    conn.close()