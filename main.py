import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import logging
from sqlalchemy import create_engine

from data_preprocessing import normalize_salary, split_address, normalize_job_title
from config import mysql_host, mysql_port, mysql_database, mysql_user, mysql_password
from visualization import positionGraph, numberOfJobsByCity, techTrend
from database import engine

# Cấu hình logging
logging.basicConfig(
    filename='app.log',  # Tên file log
    level=logging.INFO,  # Ghi nhận thông tin và lỗi
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format log
    datefmt='%Y-%m-%d %H:%M:%S'  # Định dạng thời gian
)


def main():
    filepath = 'data.csv'

    # Kiểm tra file tồn tại
    if not os.path.exists(filepath):
        logging.error(f"Tệp {filepath} không tồn tại!")
        raise FileNotFoundError(f"Tệp {filepath} không tồn tại!")

    # Đọc file CSV
    try:
        df = pd.read_csv(filepath)
        logging.info("Dữ liệu đã được đọc thành công từ file CSV.")
    except pd.errors.ParserError as e:
        logging.error(f"Lỗi định dạng CSV: {e}")
        raise ValueError(f"Tệp {filepath} không đúng định dạng: {e}")
    except Exception as e:
        logging.error(f"Lỗi không mong muốn khi đọc tệp CSV: {e}")
        raise RuntimeError(f"Lỗi không mong muốn khi đọc tệp CSV: {e}")

    # Kiểm tra dữ liệu thiếu
    if df.isnull().values.any():
        logging.error("Dữ liệu chứa giá trị null!")
        raise ValueError("Dữ liệu chứa giá trị null!")

    # Áp dụng hàm chuẩn hóa dữ liệu
    try:
        df[['min_salary', 'max_salary', 'salary_unit']] = df['salary'].apply(
            lambda x: pd.Series(normalize_salary(x))
        )
        df[['district', 'city']] = df['address'].apply(lambda x: pd.Series(split_address(x)))
        df["normalized_job_title"] = df["job_title"].apply(normalize_job_title)
        logging.info("Dữ liệu đã được chuẩn hóa thành công.")
    except Exception as e:
        logging.error(f"Lỗi khi chuẩn hóa dữ liệu: {e}")
        raise RuntimeError(f"Lỗi khi chuẩn hóa dữ liệu: {e}")

    # Chuyển đổi kiểu dữ liệu
    try:
        string_columns = ['job_title', 'company', 'salary', 'address', 'time', 
                          'link_description', 'salary_unit', 'district', 
                          'city', 'normalized_job_title']
        for col in string_columns:
            df[col] = df[col].astype('string')

        float_columns = ['min_salary', 'max_salary']
        for col in float_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
        logging.info("Chuyển đổi kiểu dữ liệu thành công.")
    except Exception as e:
        logging.error(f"Lỗi khi chuyển đổi kiểu dữ liệu: {e}")
        raise RuntimeError(f"Lỗi khi chuyển đổi kiểu dữ liệu: {e}")

    # Tính toán lương trung bình
    try:
        df['avg_salary'] = (df['min_salary'] + df['max_salary']) / 2
        if df['avg_salary'].isnull().all():
            logging.error("Không có dữ liệu lương trung bình hợp lệ để vẽ biểu đồ.")
            raise ValueError("Không có dữ liệu lương trung bình hợp lệ.")
        logging.info("Tính toán lương trung bình thành công.")
    except Exception as e:
        logging.error(f"Lỗi khi tính toán lương trung bình: {e}")
        df['avg_salary'] = None

    # Tải dữ liệu vào cơ sở dữ liệu
    try:
        df.to_sql('jobs', con=engine, if_exists='replace', index=False)
        logging.info("Dữ liệu đã được tải thành công vào cơ sở dữ liệu.")
    except Exception as e:
        logging.error(f"Lỗi trong quá trình tải dữ liệu: {e}")
    finally:
        engine.dispose()
        logging.info("Đã đóng kết nối cơ sở dữ liệu.")

    # Vẽ biểu đồ
    try:
        positionGraph(df)
        numberOfJobsByCity(df)
        techTrend(df)
        logging.info("Vẽ biểu đồ thành công.")
    except Exception as e:
        logging.error(f"Lỗi khi vẽ biểu đồ: {e}")

# Chạy chương trình
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Lỗi nghiêm trọng: {e}")
