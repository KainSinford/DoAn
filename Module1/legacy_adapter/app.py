import pandas as pd
import mysql.connector
import time
import os
import shutil

def connect_db():
    while True:
        try:
            conn = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root",
                database="noah"
            )
            return conn
        except:
            print("Đang đợi MySQL khởi động...")
            time.sleep(5)

def process():
    path = "/app/input/inventory.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            # Fix MISSING_VALUES cho Nhóm 4
            df = df.dropna(subset=['product_id', 'quantity'])
            df = df[df['quantity'] >= 0]
            
            conn = connect_db()
            cursor = conn.cursor()
            for _, row in df.iterrows():
                cursor.execute("UPDATE products SET quantity = %s WHERE product_id = %s", 
                             (int(row['quantity']), int(row['product_id'])))
            conn.commit()
            conn.close()
            
            shutil.move(path, f"/app/processed/inventory_{int(time.time())}.csv")
            print("Đã cập nhật kho thành công!")
        except Exception as e:
            print(f"Lỗi: {e}")

if name == "main":
    while True:
        process()
        time.sleep(10)
