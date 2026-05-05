import pandas as pd
import mysql.connector
import time
import os
import shutil
#pandas:đọc và xử lý file CSV
#mysql.connector:kết nối MySQL
#time:dùng sleep+timestamp
#os:kiểm tra file ttồn tại
#shutil:di chuyển file
def connect_db():
    #lỗi:mysql ko chạy,sai pass mất kết nối 
    #Hàm này đảm bảo kết nối MySQL thành công mới chạy tiếp
    #cách xử lí: retry liên tục đợi đến khi sẵn sàng
    while True:
        #lapwk vo hạn
        try:
            conn = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root",
                database="noah"
            )
            return conn
            #host="mysql" tên service trong docker comp nếu thành công thì trả về connection(ko phải localhost)
        except:
            print("Đang đợi MySQL khởi động...")
            time.sleep(5)

def process():
    path = "/app/input/inventory.csv"
    #file chứa CSV
    if os.path.exists(path):
        #ko có file = bỏ qua để tránh crash
        try:
            df = pd.read_csv(path)
            #đọc dataframe
            #File hỏng sẽ ko làm crash hệ thống
            # Fix MISSING_VALUES cho Nhóm 4
            df = df.dropna(subset=['product_id', 'quantity'])
            df = df[df['quantity'] >= 0]
            #thiếu dữ liệu,số âm
            #cách xử lí là xóa dữ liệu lỗi trước khi xử lý
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
            #lloix sql,product id ko ton tai

if _name_ == "_main_":
    while True:
        process()
        time.sleep(10)
