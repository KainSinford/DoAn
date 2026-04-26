import pandas as pd
from app.db.mysql import get_orders
from app.db.postgres import get_transactions

def get_revenue():
    orders = get_orders()
    tx = get_transactions()

    df_orders = pd.DataFrame(orders)
    df_tx = pd.DataFrame(tx)

    if df_orders.empty or df_tx.empty:
        return 0

    df = df_orders.merge(df_tx, on="order_id")

    df = df[df["status"] == "COMPLETED"]

    # Calculate revenue: sum of (quantity) from completed transactions
    # Note: if price column exists, multiply quantity * price
    revenue = int(df["quantity"].sum()) if not df.empty else 0
    return revenue
