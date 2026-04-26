import pandas as pd

def generate_report(mysql_conn, postgres_conn):
    # 1. Lấy dữ liệu
    orders = pd.read_sql("SELECT * FROM orders", mysql_conn)
    payments = pd.read_sql("SELECT * FROM payments", postgres_conn)

    # 2. Stitching (JOIN bằng pandas)
    merged = pd.merge(orders, payments, on="order_id", how="inner")

    # 3. Tính doanh thu theo user
    report = (
        merged.groupby("user_id")["total_amount"]
        .sum()
        .reset_index()
    )

    report.rename(columns={"total_amount": "total_spent"}, inplace=True)

    return report.to_dict(orient="records")
