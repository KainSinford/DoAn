import psycopg2
import os
import time

def get_connection():
    while True:
        try:
            return psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                dbname=os.getenv("POSTGRES_DB")
            )
        except:
            print("Postgres retry...")
            time.sleep(3)


def transaction_exists(order_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM transactions WHERE order_id = %s", (order_id,))
    exists = cur.fetchone()

    cur.close()
    conn.close()

    return exists


def insert_transaction(data):
    if transaction_exists(data["order_id"]):
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO transactions (order_id, user_id, product_id, quantity)
        VALUES (%s, %s, %s, %s)
    """, (
        data["order_id"],
        data["user_id"],
        data["product_id"],
        data["quantity"]
    ))

    conn.commit()
    cur.close()
    conn.close()
