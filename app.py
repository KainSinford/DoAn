import pandas as pd
import mysql.connector
import time
import os
import shutil
from mysql.connector import errorcode

# Cấu hình đường dẫn [cite: 28, 39]
INPUT_PATH = "/app/input/inventory.csv"
PROCESSED_DIR = "/app/processed/"

def connect_with_retry():
    """Hàm kết nối Database có cơ chế thử lại (Retry Challenge) """
    while True:
        try:
            conn = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "mysql"),
                user="root",
                password="root",
                database="noah"
            )
            return conn
        except mysql.connector.Error as err:
            print(f"[RETRY] Chưa thể kết nối MySQL: {err}. Thử lại sau 5 giây...")
            time.sleep(5)

def process_csv():
    if os.path.exists(INPUT_PATH):
        print(f"[INFO] Phát hiện file mới tại {time.ctime()}")
        conn = None
        try:
            # 1. Đọc dữ liệu [cite: 29]
            # Sử dụng try-except cho từng dòng để không bị crash khi gặp 'Dirty Data' [cite: 48, 211]
            df = pd.read_csv(INPUT_PATH)
            
            # 2. Xử lý MISSING_VALUES (Chiến lược Nhóm 4) 
            initial_count = len(df)
            clean_df = df.dropna(subset=['product_id', 'quantity']) 
            
            # 3. Xử lý logic nghiệp vụ: quantity < 0 [cite: 36]
            # Ghi log cảnh báo cho các dòng bị loại bỏ [cite: 36, 43]
            invalid_rows = clean_df[clean_df['quantity'] < 0]
            if not invalid_rows.empty:
                print(f"[WARN] Bỏ qua {len(invalid_rows)} dòng có số lượng âm.")
            
            clean_df = clean_df[clean_df['quantity'] >= 0]
            
            # 4. Cập nhật Database [cite: 38]
            conn = connect_with_retry()
            cursor = conn.cursor()
            
            success_count = 0
            for _, row in clean_df.iterrows():
                try:
                    cursor.execute(
                        "UPDATE products SET stock = %s WHERE id = %s", 
                        (int(row['quantity']), int(row['product_id']))
                    )
                    success_count += 1
                except Exception as row_err:
                    print(f"[ERROR] Lỗi tại dòng {row['product_id']}: {row_err}")

            conn.commit()
            
            # 5. Dọn dẹp: Di chuyển file sang thư mục processed [cite: 39, 42]
            if not os.path.exists(PROCESSED_DIR):
                os.makedirs(PROCESSED_DIR)
                
            timestamp = int(time.time())
            dest_path = os.path.join(PROCESSED_DIR, f"inventory_{timestamp}.csv")
            shutil.move(INPUT_PATH, dest_path)
            
            # 6. Log kết quả cuối cùng [cite: 43]
            skipped = initial_count - success_count
            print(f"[INFO] Hoàn thành: Cập nhật {success_count} dòng. Bỏ qua {skipped} dòng lỗi.")

        except Exception as e:
            print(f"[CRITICAL] Lỗi xử lý file: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

if __name__ == "__main__":
    print("Legacy Adapter đang chạy (Cơ chế Polling 10 giây)...")
    while True:
        process_csv()
        time.sleep(10) # Polling theo yêu cầu [cite: 33]
